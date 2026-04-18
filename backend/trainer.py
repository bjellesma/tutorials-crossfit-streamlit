import duckdb
import joblib
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import GridSearchCV, train_test_split

# Pull training data from DuckDB
conn = duckdb.connect('athletes.duckdb')
df = conn.execute("""
    SELECT age, backsq, gender, deadlift, snatch, candj, pullups, weight, height, run400, fran, helen, grace, run5k
    FROM athletes
    WHERE run400 IS NOT NULL
      AND run5k IS NOT NULL
      AND backsq IS NOT NULL
      AND deadlift IS NOT NULL
""").df()
df = df.dropna()

# Encode gender as numeric (Male=1, Female=0, others=0)
df['gender'] = df['gender'].str.lower().map({'male': 1, 'female': 0}).fillna(0)

print(f'Loaded {len(df)} athletes for training')
# Remove outliers with realistic ranges for CrossFit athletes
# run5k: 15-40 minutes (900-2400 seconds)
# backsq: 100-600 lbs
# deadlift: 150-700 lbs
# snatch: 50-350 lbs
# candj: 75-450 lbs
# pullups: 1-100 reps
# weight: 100-300 lbs
df = df[
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
print(f'Training on {len(df)} athletes after filtering outliers')

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
    'learning_rate': [0.05, 0.1, 0.2, 0.5],
    'n_estimators': [10, 50, 100, 200],
    'max_depth': [3, 4, 5, 6, 7, 8],
}

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

print('\n=== Grid Search for Best Hyperparameters ===')
print(
    f'Testing {len(param_grid["learning_rate"]) * len(param_grid["n_estimators"]) * len(param_grid["max_depth"])} combinations...\n'
)
# Train
base_model = GradientBoostingRegressor(random_state=42)
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

# Show R² scores for all combinations
print('\n=== All Parameter Combinations (sorted by R² score) ===')
results = grid_search.cv_results_
sorted_indices = results['mean_test_score'].argsort()[::-1]
for i, idx in enumerate(sorted_indices, 1):
    mean_score = results['mean_test_score'][idx]
    std_score = results['std_test_score'][idx]
    params = results['params'][idx]
    print(
        f'{i:2d}. R²={mean_score:.4f} (±{std_score:.4f}) | lr={params["learning_rate"]}, n={params["n_estimators"]:3d}, depth={params["max_depth"]}'
    )

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

# Compare with previous model settings
print('\n=== Comparison with Previous Model ===')
previous_model = GradientBoostingRegressor(
    n_estimators=10, learning_rate=0.5, max_depth=5, random_state=42, verbose=1
)
previous_model.fit(X_train, y_train)
previous_train_score = previous_model.score(X_train, y_train)
previous_test_score = previous_model.score(X_test, y_test)
print(f'Previous model: Train R²={previous_train_score:.4f}, Test R²={previous_test_score:.4f}')
print(f'Optimized model: Train R²={train_score:.4f}, Test R²={test_score:.4f}')
print(f'Improvement: {((test_score - previous_test_score) / abs(previous_test_score) * 100):.1f}%')

joblib.dump(model, 'run5k_predictor.model')
