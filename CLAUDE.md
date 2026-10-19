# CC 工作入口

先读取 `AGENTS.md`，协作规则唯一依据为 `docs/PROJECT_WORKING_RULES.md`。

Spec01、Spec02、Spec04、Spec05、Spec06 均已完成本地归档和各自唯一归档提交，最近为 Spec06 的 `e2c6d6e`。完成情况以 Git 和 Runtime 回执为准，不重复实施、审查、Verify 或归档。

**Spec09（spec09-fact-confirmation-full-query，人工确认与完整 MVP 客户查询）已通过正式 Verify（2026-10-18，full/pass），
并本地归档于 docs/openspec/changes/archive/2026-10-18-spec09-fact-confirmation-full-query/，
归档提交为唯一 Spec09 范围提交（父提交 e20a0a5，含三份主规格修订与新能力 fact-confirmation）。
不重复实施、审查、Verify 或归档。当前无活跃 change。** Spec03 继续等待杨浩侧表结构；push、部署均未执行。

**Spec10（spec10-customer-changes，客户变化查询）已通过正式 Verify（2026-10-19，full/pass），
并本地归档于 docs/openspec/changes/archive/2026-10-19-spec10-customer-changes/，
归档提交为唯一 Spec10 范围提交（父提交 5d613be，含新能力 customer-changes 与 customer-query-tools 修订）。
不重复实施、审查、Verify 或归档。当前无活跃 change。** Spec01–Spec09 已归档事实不变；Spec03 继续等待杨浩侧表结构；下一 Spec 尚未独立授权；push、部署均未执行。

具体授权与停止点以用户本轮提示词为准；不自动推进后续阶段。

集中复核后的每轮返修默认新建 CC 会话，一轮内连续完成；读取 Codex 准备的最新文件交接，接续原 change、代码和验收标准。完整方法见 `docs/PROJECT_WORKING_RULES.md`「CC 跨会话实施与集中返修」。

**代码索引规定：** 改前轻量核对工作区指纹和相关节点/依赖，同一实现/修复批次结束后统一定向刷新。能不用全量就不用，增量失败不得自动回退全量；未提交代码不能仅靠自动Hook或HEAD判断。UA已接入，完整规则及脏工作区处理见 `docs/PROJECT_WORKING_RULES.md`。

<comet-ambient-resume>
<!-- Managed by Comet. Edits inside this block may be replaced by comet init/update. -->
<!-- Contract: comet.resume_probe.v2 -->

## Comet Ambient Resume

在这个仓库中，开始处理需要改动或调查的任务前，如果可能存在活跃 Comet workflow，把当前用户请求传入只读探针：`comet resume-probe . --stdin --json`。

- 如果用户通过宿主明确调用任意 Comet Skill（例如 `@comet`、`/comet`、`@comet-native` 或 `/comet-hotfix`），显式调用优先于本恢复协议；不要运行 resume probe，直接进入被调用的 Skill。
- 如果用户通过宿主明确调用的是非 Comet 的 Skill 或斜杠命令，任务意图已由该调用明确：不要运行 resume probe，直接执行该 Skill。
- 如果你正在 Comet 流程内（包括正在等待用户回复你在流程中提出的问题），不要运行 resume probe；把这类回复（例如方案/选项选择）当作当前 change 的继续，直接按用户的选择推进。
- 只信任返回的 `workflow`、`skill` 和 `entrySource`；它们只由项目配置或无配置兼容回退决定。不得扫描或切换另一套 workflow。
- 如果 probe 返回 `auto_resume`，简短说明选中的 active change，并进入 `nextCommand` 指向的永久入口。不要把状态命令当作恢复入口直接推进。
- 如果 probe 返回 `ask_user`，只问一个简短问题并等待用户回复。
- 如果当前请求未明确调用 Comet Skill，且 probe 返回 `out_of_scope` 或 `none`，不要进入 Comet workflow。
- `out_of_scope` 或 `none` 只表示不要因为这个新请求进入 Comet workflow；它绝不表示要暂停或退出一个已在进行的 Comet 流程。
- 如果配置或状态无效且没有 `nextCommand`，停止并报告原因；不要猜测另一个 workflow。
- 不能只因为存在 active change 就把无关任务挂到该 change。Native 的未提交改动由 Native 入口检查，不由探针自动归因。
</comet-ambient-resume>
