import duckdb
import joblib
from sklearn.ensemble import ExtraTreesRegressor, GradientBoostingRegressor
from sklearn.experimental import enable_iterative_imputer  # noqa: F401
from sklearn.impute import IterativeImputer
from sklearn.model_selection import GridSearchCV, train_test_split


def _remove_outliers(df):
    """Remove outliers with realistic ranges for CrossFit athletes.

    run5k: 15-40 minutes (900-2400 seconds)
    backsq: 100-600 lbs
    deadlift: 150-700 lbs
    snatch: 50-350 lbs
    candj: 75-450 lbs
    pullups: 1-100 reps
    weight: 100-300 lbs

    Args:
        df (pd.DataFrame): DataFrame containing athlete data

    Returns:
        pd.DataFrame: DataFrame with outliers removed

    """
    return df[
        (df['age'] >= 18)
        & (df['age'] <= 65)
        & (df['run5k'] >= 900)
        & (df['run5k'] <= 2400)
        & (df['backsq'] >= 100)
        & (df['backsq'] <= 600)
        & (df['deadlift'] >= 150)
        & (df['deadlift'] <= 700)
        & (df['snatch'] >= 50)
        & (df['snatch'] <= 350)
        & (df['candj'] >= 75)
        & (df['candj'] <= 450)
        & (df['pullups'] >= 10)
        & (df['pullups'] <= 50)
        & (df['weight'] >= 100)
        & (df['weight'] <= 300)
        & (df['height'] >= 60)
        & (df['height'] <= 80)
        & (df['run400'] >= 50)
        & (df['run400'] <= 200)
        & (df['fran'] >= 200)
        & (df['fran'] <= 600)
        & (df['helen'] >= 200)
        & (df['helen'] <= 720)
        & (df['grace'] >= 200)
        & (df['grace'] <= 600)
    ]


def _impute_missing_values(df, n_neighbors=10, weights='distance'):
    """Impute missing values in numeric columns using KNN.

    Args:
        df (pd.DataFrame): DataFrame containing athlete data
        n_neighbors (int): Number of neighboring rows to use for imputation
        weights (str): 'uniform' weights all neighbors equally; 'distance' gives closer neighbors more influence

    Returns:
        pd.DataFrame: DataFrame with missing values imputed

    """
    numeric_cols = [
        'age',
        'backsq',
        'deadlift',
        'snatch',
        'candj',
        'pullups',
        'weight',
        'height',
        'run400',
        'fran',
        'helen',
        'grace',
        'run5k',
    ]
    imputer = IterativeImputer(max_iter=50, random_state=42, tol=0.001)
    df[numeric_cols] = imputer.fit_transform(df[numeric_cols])
    return df


# Pull training data from DuckDB
conn = duckdb.connect('athletes.duckdb')
df = conn.execute("""
    SELECT age, backsq, gender, deadlift, snatch, candj, pullups, weight, height, run400, fran, helen, grace, run5k
    FROM athletes LIMIT 30000
""").df()
print(f'Initial dataset contains {len(df)} athletes')

# Encode gender as numeric (Male=1, Female=0, others=0)
df['gender'] = df['gender'].str.lower().map({'male': 1, 'female': 0}).fillna(0)
print(f'Before impute: {df.head()}')
df = _impute_missing_values(df, n_neighbors=10, weights='distance')
print(f'After impute: {df.head()}')

df = _remove_outliers(df)
print(f'Cleaned dataset contains {len(df)} athletes')

# Prep features and target
X = df[
    [
        'age',
        'backsq',
        'gender',
        'deadlift',
        'snatch',
        'candj',
        'pullups',
        'weight',
        'height',
        'run400',
        'fran',
        'helen',
        'grace',
    ]
]
y = df['run5k']

# choose several combinations of hyperparameters to test
param_grid = {
    'n_estimators': [50, 100, 200, 300],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
}


X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

base_model = ExtraTreesRegressor(random_state=42)
# Grid search with 5-fold cross-validation
grid_search = GridSearchCV(
    estimator=base_model, param_grid=param_grid, scoring='r2', cv=5, n_jobs=-1, verbose=1
)

# Fit grid search
grid_search.fit(X_train, y_train)

# Show results
print('\n=== Grid Search Results ===')
print(f'Best parameters: {grid_search.best_params_}')
print(f'Best cross-validation R² score: {grid_search.best_score_:.4f}')

# Use the best model
model = grid_search.best_estimator_

# Show feature importances
print('\n=== Feature Importances ===')
feature_names = X.columns
importances = model.feature_importances_
# reverse sort by importance (highest first)
sorted_idx = importances.argsort()[::-1]
for idx in sorted_idx:
    print(f'  {feature_names[idx]:10s}: {importances[idx]:.4f} ({importances[idx] * 100:.1f}%)')

# Evaluate
train_score = model.score(X_train, y_train)
test_score = model.score(X_test, y_test)
print(f'\nTraining R² score: {train_score:.4f}')
print(f'Test R² score: {test_score:.4f}')

# Compare with baseline Gradient Boosting model
print('\n=== Comparison with Baseline Gradient Boosting ===')
previous_model = GradientBoostingRegressor(
    n_estimators=50, learning_rate=0.05, max_depth=3, random_state=42, verbose=1
)
previous_model.fit(X_train, y_train)
previous_train_score = previous_model.score(X_train, y_train)
previous_test_score = previous_model.score(X_test, y_test)
importances = previous_model.feature_importances_
# reverse sort by importance (highest first)
print('\nBaseline Gradient Boosting Feature Importances:')
sorted_idx = importances.argsort()[::-1]
for idx in sorted_idx:
    print(f'  {feature_names[idx]:10s}: {importances[idx]:.4f} ({importances[idx] * 100:.1f}%)')


print(
    f'\nGradient Boosting (baseline): Train R²={previous_train_score:.4f}, Test R²={previous_test_score:.4f}'
)
print(f'Extra Trees (optimized):      Train R²={train_score:.4f}, Test R²={test_score:.4f}')
print(
    f'\nTest R² Improvement: {((test_score - previous_test_score) / abs(previous_test_score) * 100):.1f}%'
)


joblib.dump(model, 'run5k_predictor.model')
