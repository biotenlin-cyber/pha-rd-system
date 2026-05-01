# 种子数据说明

`seed.py` 按 `code/slug` 幂等 upsert，加 `--reset` 会先 TRUNCATE 全部表。

## 评分细则（matches.yaml）

`match_score` 满分 100，由四项加和构成：

| 维度 | 权重 | 评分参考 |
| --- | --- | --- |
| `biocompat`（生物相容性） | 30 | ISO10993-I 满分；II 减 10；非医疗场景按"皮肤接触/食品接触"等折算 |
| `mechanical`（力学匹配） | 30 | 看场景下限：拉伸强度、断裂伸长、撕裂、模量 |
| `degradation`（降解匹配） | 20 | 与场景的目标降解周期一致性（土壤/海水/堆肥） |
| `processability`（工艺匹配） | 20 | 加工窗口、典型工艺与场景需求的契合度 |

`recommendation_level` 阈值建议：

- `preferred` ≥ 80
- `suitable` 60–79
- `marginal` 40–59
- `not_recommended` < 40

## 数据来源

- 牌号性能参数综合自 Bluepha / Kaneka / TianAn / Danimer Scientific 的公开数据手册与近 5 年文献综述。
- 场景市场规模为 2024 年全球估算量级，仅作 MVP 演示用，正式版本应替换为客户提供的市场情报。
