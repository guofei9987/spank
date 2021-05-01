## spank

Easier implement based on pandas

Select:
```python
sdf.select_expr('name as name1', '*', 'type as style_type',
                sdf.feature1 + 1,
                F.Value(np.sin(sdf.feature2)).alias("feature4"),
                F.Value(1))
```

Or filter
```python
sdf.filter_expr((sdf.sex == 'female') & (sdf.feature2 > 0.1))
```