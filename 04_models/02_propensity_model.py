import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.preprocessing import LabelEncoder

# Ensure the 'df' DataFrame from the BigQuery export is available
# If not, you would re-run the BigQuery query or load it from a saved file.
# For this script, we assume 'df' is already in memory from the previous step.

print("Preparing data for propensity modeling...")

# Make a copy to avoid modifying the original DataFrame
model_df = df.copy()

# --- 1. Feature Engineering and Preprocessing ---

# Handle categorical features using one-hot encoding
# Exclude 'user_id' as it's an identifier
categorical_cols = ['country', 'intent_level']
model_df = pd.get_dummies(model_df, columns=categorical_cols, drop_first=True)

# Handle missing values in numerical features
# 'age' was from users_df and handled there. 'swipe_to_match_ratio' and 'match_rate_30d' have NaNs from SAFE_DIVIDE.
# Fill NaNs with 0, implying no activity or very low ratio, which is a reasonable imputation for these metrics.
model_df['swipe_to_match_ratio'] = model_df['swipe_to_match_ratio'].fillna(0)
model_df['match_rate_30d'] = model_df['match_rate_30d'].fillna(0)

# Ensure `is_paying` and `verification_passed` are numeric (Int64 can be used directly by models, but float is safer)
model_df['is_paying'] = model_df['is_paying'].astype(float)
model_df['verification_passed'] = model_df['verification_passed'].astype(float)

# --- 2. Define Target and Features ---
# For this demonstration, let's predict if a user is_paying
X = model_df.drop(['user_id', 'is_paying'], axis=1)
y = model_df['is_paying']

# Ensure all columns in X are numeric (pd.get_dummies should have handled this for categoricals)
# Check for any remaining non-numeric columns that might have slipped through
non_numeric_cols = X.select_dtypes(include=['object', 'category']).columns
if len(non_numeric_cols) > 0:
    print(f"Warning: Non-numeric columns found: {non_numeric_cols}. Attempting to encode.")
    for col in non_numeric_cols:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col])

# --- 3. Split Data ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=RANDOM_SEED, stratify=y)

print("Data split into training and testing sets.")
print(f"Training set shape: {X_train.shape}")
print(f"Test set shape: {X_test.shape}")

# --- 4. Train Model ---
print("Training RandomForestClassifier...")
model = RandomForestClassifier(n_estimators=100, random_state=RANDOM_SEED, class_weight='balanced') # Use class_weight for imbalanced target
model.fit(X_train, y_train)
print("Model training complete.")

# --- 5. Evaluate Model ---
print("Evaluating model performance...")
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

print("
Classification Report:")
print(classification_report(y_test, y_pred))

print("
ROC AUC Score:", roc_auc_score(y_test, y_proba))

print("
Top 10 Feature Importances:")
feature_importances = pd.Series(model.feature_importances_, index=X.columns)
print(feature_importances.nlargest(10))

# Add propensity scores to the original model_df for potential further use
model_df['propensity_is_paying'] = model.predict_proba(X)[:, 1]

print("
Propensity scores added to the DataFrame.")
print(model_df[['user_id', 'is_paying', 'propensity_is_paying']].head())
