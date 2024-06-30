import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import math

with open('roc_2d_siamese.txt', 'r+') as f:
    roc_2d_siamese = f.read()

with open('roc_3d_siamese.txt', 'r+') as f:
    roc_3d_siamese = f.read()

with open('roc_2d_triplet.txt', 'r+') as f:
    roc_2d_triplet = f.read()

with open('roc_3d_triplet.txt', 'r+') as f:
    roc_3d_triplet = f.read()

with open('roc_concat_siamese.txt', 'r+') as f:
    roc_concat_siamese = f.read()

with open('roc_concat_triplet.txt', 'r+') as f:
    roc_concat_triplet = f.read()

with open('roc_2d_classify.txt', 'r+') as f:
    roc_2d_classify = f.read()

with open('roc_3d_classify.txt', 'r+') as f:
    roc_3d_classify = f.read()

with open('roc_concat_classify.txt', 'r+') as f:
    roc_concat_classify = f.read()

def spilt_result_classify(text):
    loss_train = []
    loss_valid = []
    acc_train = []
    acc_valid = []
    roc_train_dis= []
    roc_valid_dis = []    
    roc_train_cos = []
    roc_valid_cos = []
    lines = text.split("\n")
    for line in lines:
        if line.startswith("Train"):
            if len(loss_valid)<len(loss_train):
                loss_valid.append(loss_valid[-1])
                acc_valid.append(acc_valid[-1])
            loss_train.append(float(line.split()[5]))
            acc_train.append(float(line.split()[11]))
        elif line.startswith("Valid"):
            loss_valid.append(float(line.split()[5]))
            acc_valid.append(float(line.split()[11]))
        elif line.startswith("---Epoch:"):
            if 'Train' in line:
                roc_train_dis.append(float(line.split()[6]))
                roc_train_cos.append(float(line.split()[10]))
            elif 'Validation' in line:
                roc_valid_dis.append(float(line.split()[6]))
                roc_valid_cos.append(float(line.split()[10]))
    return loss_train, loss_valid, acc_train, acc_valid, roc_train_dis, roc_valid_dis, roc_train_cos, roc_valid_cos

def spilt_result(text):
    loss_train = []
    loss_valid = []
    roc_train_dis= []
    roc_valid_dis = []    
    roc_train_cos = []
    roc_valid_cos = []
    lines = text.split("\n")
    for line in lines[10:]:
        if line.startswith("Epoch:"):
            if 'Train' in line:
                loss_train.append(float(line.split(' ')[-1]))
            elif 'Validation' in line:
                loss_valid.append(float(line.split(' ')[-1]))
        elif line.startswith("---Epoch:"):
            if 'Train' in line:
                roc_train_dis.append(float(line.split()[6]))
                roc_train_cos.append(float(line.split()[10]))
            elif 'Validation' in line:
                roc_valid_dis.append(float(line.split()[6]))
                roc_valid_cos.append(float(line.split()[10]))
    return loss_train, loss_valid, roc_train_dis, roc_valid_dis, roc_train_cos, roc_valid_cos

loss_train, loss_valid, roc_train_dis, roc_valid_dis, roc_train_cos, roc_valid_cos = spilt_result(roc_2d_triplet)
# loss_train, loss_valid, roc_train_dis, roc_valid_dis, roc_train_cos, roc_valid_cos = spilt_result(roc_3d_triplet)
# loss_train, loss_valid, roc_train_dis, roc_valid_dis, roc_train_cos, roc_valid_cos = spilt_result(roc_concat_triplet)

# loss_train, loss_valid, acc_train, acc_valid, roc_train_dis, roc_valid_dis, roc_train_cos, roc_valid_cos = spilt_result_classify(roc_concat_classify)

data = {
    'Epoch': range(9, len(roc_train_dis)*10, 10),
    'ROC_train': roc_train_dis,
    'ROC_valid': roc_valid_dis
}

df = pd.DataFrame(data)

# Melt DataFrame để có thể vẽ biểu đồ
df_melted = pd.melt(df, id_vars=['Epoch'], var_name='Type', value_name='Value')

# Tìm epoch có loss_train nhỏ nhất và giá trị loss_train tương ứng
min_loss_train_row = df.loc[df['ROC_train'].idxmax()]
print("Thông tin của epoch có ROC_train lớn nhất:")
print(min_loss_train_row)

# Tìm epoch có loss_valid nhỏ nhất và giá trị loss_valid tương ứng
min_loss_valid_row = df.loc[df['ROC_valid'].idxmax()]
print("Thông tin của epoch có ROC_valid lớn nhất:")
print(min_loss_valid_row)


# Vẽ biểu đồ
plt.figure(figsize=(10, 6))
sns.lineplot(x='Epoch', y='Value', hue='Type', data=df_melted)
plt.title('Training and Validation Metrics Over Epochs')
plt.xlabel('Epoch')
plt.ylabel('Value')
plt.legend(title='Metrics')
plt.show()

data = {
    'Epoch': range(9, len(roc_train_cos)*10, 10),
    'ROC_train': roc_train_cos,
    'ROC_valid': roc_valid_cos
}

df = pd.DataFrame(data)

# Melt DataFrame để có thể vẽ biểu đồ
df_melted = pd.melt(df, id_vars=['Epoch'], var_name='Type', value_name='Value')

# Tìm epoch có loss_train nhỏ nhất và giá trị loss_train tương ứng
min_loss_train_row = df.loc[df['ROC_train'].idxmax()]
print("Thông tin của epoch có ROC_train lớn nhất:")
print(min_loss_train_row)

# Tìm epoch có loss_valid nhỏ nhất và giá trị loss_valid tương ứng
min_loss_valid_row = df.loc[df['ROC_valid'].idxmax()]
print("Thông tin của epoch có ROC_valid lớn nhất:")
print(min_loss_valid_row)


# Vẽ biểu đồ
plt.figure(figsize=(10, 6))
sns.lineplot(x='Epoch', y='Value', hue='Type', data=df_melted)
plt.title('Training and Validation Metrics Over Epochs')
plt.xlabel('Epoch')
plt.ylabel('Value')
plt.legend(title='Metrics')
plt.show()

data = {
    'Epoch': range(1, len(loss_train)+1),
    'Loss_train': loss_train,
    'Loss_valid': loss_valid
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

data = {
    'Epoch': range(1, len(loss_train)+1),
    'Acc_train': acc_train,
    'Acc_valid': acc_valid
}

df = pd.DataFrame(data)

# Melt DataFrame để có thể vẽ biểu đồ
df_melted = pd.melt(df, id_vars=['Epoch'], var_name='Type', value_name='Value')

# Tìm epoch có loss_train nhỏ nhất và giá trị loss_train tương ứng
min_loss_train_row = df.loc[df['Acc_train'].idxmax()]
print("Thông tin của epoch có Loss_train nhỏ nhất:")
print(min_loss_train_row)

# Tìm epoch có loss_valid nhỏ nhất và giá trị loss_valid tương ứng
min_loss_valid_row = df.loc[df['Acc_valid'].idxmax()]
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