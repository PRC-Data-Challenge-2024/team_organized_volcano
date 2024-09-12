import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# Assuming X_tabular is your 12 scalar features
# X_trajectory is a list of tensors, each representing the 7 time-series features for a flight, where each tensor has a variable sequence length
# y is the target variable (TOW)

# Split the data into train and test sets
X_tab_train, X_tab_test, X_traj_train, X_traj_test, y_train, y_test = train_test_split(
    X_tabular, X_trajectory, y, test_size=0.2, random_state=42
)

# Standardize the scalar features
scaler = StandardScaler()
X_tab_train = scaler.fit_transform(X_tab_train)
X_tab_test = scaler.transform(X_tab_test)

# Convert to PyTorch tensors
X_tab_train_tensor = torch.tensor(X_tab_train, dtype=torch.float32)
X_tab_test_tensor = torch.tensor(X_tab_test, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train.values, dtype=torch.float32).view(-1, 1)
y_test_tensor = torch.tensor(y_test.values, dtype=torch.float32).view(-1, 1)

# Define the neural network architecture
class TOWNet(nn.Module):
    def __init__(self, input_dim_tabular, input_dim_trajectory, hidden_dim_lstm, lstm_layers=1):
        super(TOWNet, self).__init__()

        # Feedforward for the scalar features
        self.fc1 = nn.Linear(input_dim_tabular, 128)
        self.fc2 = nn.Linear(128, 64)

        # LSTM for the time-series trajectory data
        self.lstm = nn.LSTM(input_dim_trajectory, hidden_dim_lstm, lstm_layers, batch_first=True)

        # Fully connected layers to combine the outputs from both parts
        self.fc_combined = nn.Linear(hidden_dim_lstm + 64, 64)
        self.fc_out = nn.Linear(64, 1)
        self.relu = nn.ReLU()

    def forward(self, x_tabular, x_trajectory):
        # Feedforward for scalar features
        x_tab = self.relu(self.fc1(x_tabular))
        x_tab = self.relu(self.fc2(x_tab))

        # LSTM for trajectory data
        lstm_out, (hn, cn) = self.lstm(x_trajectory)
        lstm_out = hn[-1]  # Use the final hidden state of the LSTM

        # Combine both outputs
        x_combined = torch.cat((x_tab, lstm_out), dim=1)
        x_combined = self.relu(self.fc_combined(x_combined))

        # Output layer
        output = self.fc_out(x_combined)
        return output

# Hyperparameters
input_dim_tabular = X_tab_train_tensor.shape[1]  # 12 scalar features
input_dim_trajectory = 7  # 7 time-series trajectory features
hidden_dim_lstm = 64  # LSTM hidden dimension

# Instantiate the model
model = TOWNet(input_dim_tabular, input_dim_trajectory, hidden_dim_lstm)

# Loss function and optimizer
criterion = nn.MSELoss()  # RMSE will be calculated separately from MSE
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training loop
epochs = 100
for epoch in range(epochs):
    model.train()

    total_loss = 0
    for i in range(len(X_tab_train_tensor)):
        x_tab = X_tab_train_tensor[i].unsqueeze(0)
        x_traj = torch.tensor(X_traj_train[i], dtype=torch.float32).unsqueeze(0)  # Adding batch dimension

        # Forward pass
        outputs = model(x_tab, x_traj)
        loss = criterion(outputs, y_train_tensor[i].unsqueeze(0))

        # Backward pass and optimization
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    if (epoch + 1) % 10 == 0:
        print(f'Epoch [{epoch+1}/{epochs}], Loss: {total_loss/len(X_tab_train_tensor):.4f}')

# Evaluate on test set
model.eval()
total_test_loss = 0
with torch.no_grad():
    for i in range(len(X_tab_test_tensor)):
        x_tab = X_tab_test_tensor[i].unsqueeze(0)
        x_traj = torch.tensor(X_traj_test[i], dtype=torch.float32).unsqueeze(0)

        y_pred = model(x_tab, x_traj)
        test_loss = criterion(y_pred, y_test_tensor[i].unsqueeze(0))
        total_test_loss += test_loss.item()

# Calculate RMSE
rmse = torch.sqrt(torch.tensor(total_test_loss / len(X_tab_test_tensor)))
print(f'Test RMSE: {rmse.item():.4f}')
