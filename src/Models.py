import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import MessagePassing

#lat and lon
POS_DIM = 2

class PositionalMessagePassing(MessagePassing):
    """
    Message Passing Layer that incorporates relative position information.
    """
    def __init__(self, in_channels, out_channels, pos_dim=POS_DIM, **kwargs):
        super().__init__(aggr='mean', **kwargs)
        
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.pos_dim = pos_dim

        #Input: neighbor features (in_channels) + relative position (pos_dim)
        message_input_dim = self.in_channels + self.pos_dim
        #Linear transformation directly to out channels, followed by activation function
        self.message_mlp = nn.Sequential(
            nn.Linear(message_input_dim, self.out_channels),
            nn.PReLU()
        )
        #Combining original node features and aggregated messages
        #Input: original node features (in_channels) + aggregated messages (out channels)
        self.update_mlp = nn.Sequential(
            nn.Linear(self.in_channels + self.out_channels, self.out_channels),
            nn.PReLU() 
        )

    def forward(self, x, edge_index, pos):
        #Start message passing. Pass 'pos' along with 'x'
        return self.propagate(edge_index, x=x, pos=pos)

    def message(self, x_j, pos_i, pos_j):
        #Construct message

        #Calculate relative position
        rel_pos = pos_i - pos_j

        #Concatenate neighbor features and relative position
        message_features = torch.cat([x_j, rel_pos], dim=-1)
        
        #Process through MLP
        message = self.message_mlp(message_features) 
        return message

    def update(self, aggr_out, x):
        #Update node embeddings

        #Concatenate original node features and aggregated messages
        update_features = torch.cat([x, aggr_out], dim=-1)

        #Process through the udpated MLP
        updated_embedding = self.update_mlp(update_features)
        return updated_embedding

    def __repr__(self):
        return f'{self.__class__.__name__}({self.in_channels}, {self.out_channels})'

#GNN Model
class CustomGNN(torch.nn.Module):
    """
    5-layer GNN model
    """
    def __init__(self, in_features, hidden_channels, out_channels, pos_dim=POS_DIM, indices_to_keep=None):
        super().__init__()
        
        # Save the specific indices depending on model
        self.indices_to_keep = indices_to_keep 
        
        self.conv1 = PositionalMessagePassing(in_features, hidden_channels, pos_dim=pos_dim)
        self.activation1 = nn.PReLU() 

        self.conv2 = PositionalMessagePassing(hidden_channels, hidden_channels, pos_dim=pos_dim) 
        self.activation2 = nn.PReLU() 

        self.conv3 = PositionalMessagePassing(hidden_channels, hidden_channels, pos_dim=pos_dim)
        self.activation3 = nn.PReLU() 

        self.conv4 = PositionalMessagePassing(hidden_channels, hidden_channels, pos_dim=pos_dim)
        self.activation4 = nn.PReLU() 

        self.conv5 = PositionalMessagePassing(hidden_channels, hidden_channels, pos_dim=pos_dim)
        self.activation5 = nn.PReLU()

        self.final_lin = nn.Linear(hidden_channels, out_channels)

    def forward(self, data):
        # Slice the data based on the model's assigned indices
        if self.indices_to_keep is not None:
            x = data.x[:, self.indices_to_keep]
        else:
            x = data.x  #Use all features if no indices are provided
            
        edge_index, pos = data.edge_index, data.pos
        
        #Layer 1
        x = self.activation1(self.conv1(x, edge_index, pos))
        
        #Layer 2
        x = self.activation2(self.conv2(x, edge_index, pos))
        
        #Layer 3
        x = self.activation3(self.conv3(x, edge_index, pos))
        
        #Layer 4
        x = self.activation4(self.conv4(x, edge_index, pos))
        
        #Layer 5
        x = self.activation5(self.conv5(x, edge_index, pos))     
        
        #Layer final prediction layer
        x = self.final_lin(x)

        return x #output shape: [num_nodes_in_batch, out_channels]
        