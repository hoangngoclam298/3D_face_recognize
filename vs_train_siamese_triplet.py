import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import math

with open('train_2d_siamese.txt', 'r+') as f:
    train_2d_siamese = f.read()

with open('train_3d_siamese.txt', 'r+') as f:
    train_3d_siamese = f.read()

with open('train_2d_triplet.txt', 'r+') as f:
    train_2d_triplet = f.read()

with open('train_3d_triplet.txt', 'r+') as f:
    train_3d_triplet = f.read()

with open('train_concat_siamese.txt', 'r+') as f:
    train_concat_siamese = f.read()

with open('train_concat_triplet.txt', 'r+') as f:
    train_concat_triplet = f.read()

with open('train_2d_siamese_1e-4.txt', 'r+') as f:
    train_2d_siamese_1e = f.read()

def spilt_result(text):
    loss_train = []
    loss_valid = []
    epochs = text.split("\n")
    for i in range(10, int(len(epochs)/2)):
        line_train, line_val = epochs[2*i], epochs[2*i+1]
        loss_train.append(float(line_train.split(' ')[-1]))
        loss_valid.append(float(line_val.split(' ')[-1]))
    return loss_train, loss_valid

loss_train, loss_valid = spilt_result(train_2d_siamese_1e)

data = {
    'Epoch': range(1, len(loss_train) + 1),
    'Loss_train': loss_train,
    'Loss_valid': loss_valid,
}

df = pd.DataFrame(data)

# Melt DataFrame để có thể vẽ biểu đồ
df_melted = pd.melt(df, id_vars=['Epoch'], var_name='Type', value_name='Value')

# Tìm epoch có loss_train nhỏ nhất và giá trị loss_train tương ứng
min_loss_train_row = df.loc[df['Loss_train'].idxmin()]
print("Thông tin của epoch có Loss_train nhỏ nhất:")
print(min_loss_train_row)

# Tìm epoch có loss_valid nhỏ nhất và giá trị loss_valid tương ứng
min_loss_valid_row = df.loc[df['Loss_valid'].idxmin()]
print("Thông tin của epoch có Loss_valid nhỏ nhất:")
print(min_loss_valid_row)

# Vẽ biểu đồ
plt.figure(figsize=(10, 6))
sns.lineplot(x='Epoch', y='Value', hue='Type', data=df_melted)
plt.title('Training and Validation Metrics Over Epochs')
plt.xlabel('Epoch')
plt.ylabel('Value')
plt.legend(title='Metrics')
plt.show()