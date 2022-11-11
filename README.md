# Idea

## Results

Disabled GC shows better performance:

![generational results](generations.png)

## Process

Stage 1 will create a tree using the builtin dict structure.

```json
{0: 0.0,
 1: 0,
 2: [],
 3: {4: None,
     5: (),
     6: 0.0,
     7: 0,
     8: [],
     9: {10: None,
         11: (),
         12: 0.0,
         13: 0,
         14: [],
         15: {16: None,
              17: (),
              18: 0.0,
              19: 0,
              20: [],
    ...
}
```

Stage 2 will go through and for each list in the tree, add the parent dictionary as an item

```json
{0: 0.0,
 1: 0,
 2: [<Recursion on dict with id=4354355376>],
 3: {4: None,
     5: (),
     6: 0.0,
     7: 0,
     8: [<Recursion on dict with id=4354355568>],
     9: {10: None,
         11: (),
         12: 0.0,
         13: 0,
         14: [<Recursion on dict with id=4354357968>],
         15: {16: None,
              17: (),
              18: 0.0,
              19: 0,
              20: [{...}],
              21: {22: None, 23: (), 24: 0.0, 25: 0, 26: [...], 27: {...}}}}}}
```

Stage 3 will then go through and reverse the process of stage 2:

```json
{0: 0.0,
 1: 0,
 2: [],
 3: {4: None,
     5: (),
     6: 0.0,
     7: 0,
     8: [],
     9: {10: None,
         11: (),
         12: 0.0,
         13: 0,
         14: [],
         15: {16: None,
              17: (),
              18: 0.0,
              19: 0,
              20: [],
              21: {22: None, 23: (), 24: 0.0, 25: 0, 26: [], 27: {...}}}}}}
```
