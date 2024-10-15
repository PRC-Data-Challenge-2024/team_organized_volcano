import torch
import torch.nn as nn


class SimpleNN(nn.Module):
    def __init__(self, num_categories, category_embedding_size, continuous_size, hidden_size, sequence_hidden_size):
        super(SimpleNN, self).__init__()

        # Embedding layer for categorical features
        self.embedding_layer = nn.Embedding(num_categories, category_embedding_size)

        # Linear layer for the continuous features (5 continuous features)
        self.continuous_layer = nn.Linear(continuous_size, hidden_size)

        # Input layer for the sequence data (6 floats + 1 timestep index)
        self.sequence_layer = nn.LSTM(input_size=7, hidden_size=sequence_hidden_size, batch_first=True)

        # Combine both inputs (embedding + continuous features + sequence features)
        self.combined_layer = nn.Linear(category_embedding_size * 8 + hidden_size, hidden_size)

        # Additional hidden layer
        self.hidden_layer = nn.Linear(hidden_size, hidden_size)

        # Output layer predicting a float
        self.output_layer = nn.Linear(hidden_size, 1)

    def forward(self, categorical_input, continuous_input, sequence_input):
        # Process categorical input (8 categorical features)
        embedded_cat = [self.embedding_layer(categorical_input[:, i]) for i in range(categorical_input.size(1))]
        embedded_cat = torch.cat(embedded_cat, dim=1)  # Concatenate the embeddings

        # Process continuous input
        continuous_out = torch.relu(self.continuous_layer(continuous_input))

        # Combine categorical and continuous features
        feature_combined = torch.cat((embedded_cat, continuous_out), dim=1)

        # Process the sequence input (6 floats + 1 timestep index)
        sequence_out, _ = self.sequence_layer(sequence_input)
        sequence_out = sequence_out[:, -1, :]  # Take the last output of the LSTM

        # Combine all inputs
        combined = torch.cat((feature_combined, sequence_out), dim=1)
        combined_out = torch.relu(self.combined_layer(combined))

        # Pass through hidden layer
        hidden_out = torch.relu(self.hidden_layer(combined_out))

        # Output prediction
        output = self.output_layer(hidden_out)
        return output


# Example of initializing the model
num_categories = 50  # Assuming each categorical feature has 50 possible categories
category_embedding_size = 8
continuous_size = 5  # 5 continuous features out of 13 total features
hidden_size = 64
sequence_hidden_size = 32

model = SimpleNN(num_categories, category_embedding_size, continuous_size, hidden_size, sequence_hidden_size)

# Example forward pass
categorical_input = torch.randint(0, num_categories, (32, 8))  # batch_size = 32, 8 categorical features
continuous_input = torch.randn(32, continuous_size)  # batch_size = 32, 5 continuous features
sequence_input = torch.randn(32, 5, 7)  # batch_size = 32, sequence length = 5, 7 features (6 floats + 1 timestep)

output = model(categorical_input, continuous_input, sequence_input)
print(output.shape)  # Output will be of shape [32, 1] (batch_size, output_size)
