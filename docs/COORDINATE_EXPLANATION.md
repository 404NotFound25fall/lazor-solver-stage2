# Lazor 坐标系统详解

## 📐 Half-Block 坐标系统

根据注释说明：
```
Grid will start at top left being 0, 0
Step size is by half blocks
Thus, this leads to even numbers indicating
the rows/columns between blocks, and odd numbers
intersecting blocks.
```

### 正确理解

对于 2x2 网格（方块）：

```
half-block 坐标系统：

   0    1    2    3    4
0  ----  ----  ----  ----
   |    |    |    |
1  ---- • ---- • ----      • = 方块中心
   |    |    |    |
2  ----  ----  ----  ----
   |    |    |    |
3  ---- • ---- • ----      • = 方块中心
   |    |    |    |
4  ----  ----  ----  ----
```

- **奇数坐标** (1, 3, 5, 7, ...) = 方块中心
- **偶数坐标** (0, 2, 4, 6, ...) = 方块之间的间隙

### 网格索引到 half-block 坐标

- 网格 (0, 0) → half-block (1, 1)
- 网格 (0, 1) → half-block (3, 1)
- 网格 (1, 0) → half-block (1, 3)
- 网格 (r, c) → half-block (2*c+1, 2*r+1)

### half-block 坐标到网格索引

- half-block (x, y) 是奇数 → 网格 ((y-1)/2, (x-1)/2)
- half-block (x, y) 是偶数 → 不在方块上，在间隙中

## ❌ 我们当前的错误

```python
grid_row = y  # 错误！
grid_col = x  # 错误！
```

应该是：
```python
if x % 2 == 1 and y % 2 == 1:  # 奇数坐标
    grid_row = (y - 1) // 2
    grid_col = (x - 1) // 2
```

## 💡 需要修复

模拟器的坐标转换逻辑需要完全重写！

