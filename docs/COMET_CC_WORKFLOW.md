# Comet 与 CC 交接入口

当前协作规则见 [PROJECT_WORKING_RULES.md](PROJECT_WORKING_RULES.md)。

1. Codex 在当前 `docs/specNN/EXECUTION_PLAN.md` 写规划及只读审阅提示词。
2. 用户在新 CC 会话提交短提示词，CC 只读审阅并返回意见。
3. Codex 把反馈处理写进 `review-notes.md`，修订同一份规划。
4. 再单独交付规格编写提示词。CC 通过 Comet Classic 在 `docs/openspec/` 创建或续接正式规格，写完及校验后停止。
5. Codex 读取实际 proposal/specs/design/tasks，集中检验最小范围与一致性。
6. 检验通过后才另给实施提示词，CC 连续完成当前范围、最小自检和修复，集中交付。
7. Codex 集中复核，稳定证据复用；提交、归档及下一 Spec 按独立授权执行。

## 当前工具状态

2026-10-09只读核对：全局 Comet 0.4.4、OpenSpec 1.2.0。CRM 没有 `.comet/` 或项目级 CC 接入，不能把 audio 的已安装/已批准状态套到这里。

2026-10-10：Spec01正式规格、CC实施、Codex集中复核、正式Verify及本地归档全部完成，任务9/9，唯一本地归档提交5b81e8d。Runtime交付核对complete，selection已清除，不重复已有检查或归档。Spec02随后按同一流程另行授权执行。

2026-10-11：Spec02（spec02-customer-query-tools）正式规格、CC实施、Codex集中复核、正式Verify及本地归档全部完成，任务10/10，唯一本地归档提交ec33a92。Runtime交付核对complete，selection已清除，不重复已有检查或归档；UA接入与首次建图产物随该提交入库。下一Spec尚未授权，无待执行交接入口。

正式规格实际根为 `docs/openspec/`，当前没有活跃change；Spec01、Spec02证据分别在 `docs/openspec/changes/archive/2026-10-10-spec01-customer-foundation/`、`docs/openspec/changes/archive/2026-10-11-spec02-customer-query-tools/`。早期规格保存在 `docs/spec01/drafts/openspec/`，不作为活跃change。
