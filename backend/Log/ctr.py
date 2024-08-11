import torch
import torch.nn as nn
import torch.optim as optim


# 定义一个简单的CTR模型
class SimpleCTRModel(nn.Module):
    def __init__(self, num_features, embedding_dim):
        super(SimpleCTRModel, self).__init__()
        # 嵌入层
        self.embedding = nn.Embedding(num_features, embedding_dim)
        # 前馈神经网络
        self.fc1 = nn.Linear(embedding_dim, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.embedding(x).view(x.size(0), -1)  # 嵌入层输出并展平
        x = torch.relu(self.fc1(x))  # 激活函数ReLU
        x = torch.relu(self.fc2(x))  # 激活函数ReLU
        x = self.fc3(x)
        x = self.sigmoid(x)  # 输出层使用Sigmoid激活函数
        return x


# 示例数据
num_features = 1000  # 特征数量
embedding_dim = 32  # 嵌入维度
model = SimpleCTRModel(num_features, embedding_dim)

# 损失函数和优化器
criterion = nn.BCELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 示例输入和目标
inputs = torch.randint(0, num_features, (10,))  # 10个样本，每个样本是一个特征ID
targets = torch.randint(0, 2, (10, 1)).float()  # 目标为0或1

# 训练步骤
model.train()
for epoch in range(10):  # 训练10个epoch
    optimizer.zero_grad()
    outputs = model(inputs)
    loss = criterion(outputs, targets)
    loss.backward()
    optimizer.step()
    print(f'Epoch {epoch + 1}, Loss: {loss.item()}')
