import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

with open('train_2d_ft.txt', 'r+') as f:
    train_2d_ft = f.read()

with open('train_3d_ft.txt', 'r+') as f:
    train_2d_ft = f.read()

with open('train_2d_nft.txt', 'r+') as f:
    train_2d_nft = f.read()

with open('train_3d_nft.txt', 'r+') as f:
    train_3d_nft = f.read()

with open('train_2d_aug.txt', 'r+') as f:
    train_2d_aug = f.read()

with open('train_3d_aug.txt', 'r+') as f:
    train_3d_aug = f.read()


def spilt_result(text):
    loss_train = []
    acc_train = []
    loss_valid = []
    acc_valid = []
    epochs = text.split("Epoch")
    for epoch in epochs[100::5]:
        lines = epoch.split('\n')
        loss_train.append(float(lines[2][30:36]))
        acc_train.append(float(lines[2][64:70]))
        loss_valid.append(float(lines[3][30:36]))
        acc_valid.append(float(lines[3][64:70]))
    return loss_train, acc_train, loss_valid, acc_valid

loss_train, acc_train, loss_valid, acc_valid = spilt_result(train_3d_aug)

data = {
    'Epoch': range(1, len(loss_train) + 1),
    'Loss_train': loss_train,
    'Loss_valid': loss_valid,
    'Acc_train': acc_train,
    'Acc_valid': acc_valid
}
df = pd.DataFrame(data)

df = pd.DataFrame(data)

# Melt DataFrame để có thể vẽ biểu đồ
df_melted = pd.melt(df, id_vars=['Epoch'], var_name='Type', value_name='Value')

# Vẽ biểu đồ
plt.figure(figsize=(10, 6))
sns.lineplot(x='Epoch', y='Value', hue='Type', data=df_melted)
plt.title('Training and Validation Metrics Over Epochs')
plt.xlabel('Epoch')
plt.ylabel('Value')
plt.legend(title='Metrics')
plt.show()