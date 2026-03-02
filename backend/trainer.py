import duckdb
import joblib
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split

# Pull training data from DuckDB
conn = duckdb.connect('athletes.duckdb')
df = conn.execute("""
    SELECT age, backsq, gender, deadlift, snatch, candj, pullups, weight, run5k
    FROM athletes
    WHERE run5k IS NOT NULL
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
    & (df['pullups'] >= 1)
    & (df['pullups'] <= 100)
    & (df['weight'] >= 100)
    & (df['weight'] <= 300)
]
print(f'Training on {len(df)} athletes after filtering outliers')

# Prep features and target
X = df[['age', 'backsq', 'gender', 'deadlift', 'snatch', 'candj', 'pullups', 'weight']]
y = df['run5k']

# Train
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
model = GradientBoostingRegressor(
    n_estimators=10, learning_rate=0.4, verbose=1, max_depth=5, random_state=42
)
model.fit(X_train, y_train)

# todo add feature importance and partial dependence plots to understand model behavior

# Evaluate
train_score = model.score(X_train, y_train)
test_score = model.score(X_test, y_test)
print(f'\nTraining R² score: {train_score:.4f}')
print(f'Test R² score: {test_score:.4f}')

joblib.dump(model, 'run5k_predictor.model')
