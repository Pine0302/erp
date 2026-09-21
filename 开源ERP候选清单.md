# 印刷厂 ERP 开源方案候选清单

> 依据 `docs/印刷厂ERP管理系统完整软件开发需求方案.docx` 与 `docs/印刷厂ERP管理系统完整软件开发需求规格说明书1.docx` 提炼的核心诉求：**客户合同额度管控 + 多工位工序流转（印刷→切纸→装订→打包→运输→签收）+ 总厂/驻点多仓库 + 计件绩效 + 多级数据隔离 + 三端（PC/客户小程序/官网）**。
> 完全对口"印刷细分行业"的开源极少，下面按"行业匹配度"由高到低列出，**括号中百分比为本人对该项目覆盖七大模块的粗略主观评估**，仅供参考。
> 检索日期：2026-08-22，工具：`gh search repos`

---

## 一、⭐ 最对口：印刷行业专用（强烈推荐优先评估）

| 项目 | ⭐ | 语言/栈 | 仓库 | 覆盖度 | 说明 |
|---|---|---|---|---|---|
| **jiumierp（小象智慧ERP）** | 9 | Java | [`chenzhitao/jiumierp`](https://github.com/chenzhitao/jiumierp) | **★★★★★ 80%** | 多个印刷厂ERP成功上线改造而成，**细分领域就是印刷厂管理**，功能齐全、可直接部署、二次开发。模块覆盖采购、销售、库存、生产（工序）、财务、客户管理，最接近需求。 |
| **ghprint-cms（光华印刷库存）** | 2 | Java | [`hwedwin/ghprint-cms`](https://github.com/hwedwin/ghprint-cms) | ★★ 30% | 印刷库存管理专用，体量小可作参考。 |
| **PrintShop** | 1 | Python | [`amikuo/PrintShop`](https://github.com/amikuo/PrintShop) | ★★ 25% | 印刷店管理系统，参考价值。 |
| **Java_PrinterManagementSoftware** | 0 | Java | [`yhnbgfd/Java_PrinterManagementSoftware`](https://github.com/yhnbgfd/Java_PrinterManagementSoftware) | ★ 20% | 印刷厂管理软件1.0，学习用途。 |
| **rongzheng-print（融正印刷）** | 0 | HTML | [`biyuhang88-dot/rongzheng-print`](https://github.com/biyuhang88-dot/rongzheng-print) | ★ 20% | 融正印刷生产管理系统。 |
| **Xzavier-zjf MES（注塑/印刷）** | 0 | Vue | [`Xzavier-zjf/MES`](https://github.com/Xzavier-zjf/MES) | ★★ 30% | 注塑/印刷生产管理系统。 |

> **建议**：如果决定不全新定制，`jiumierp` 是几乎唯一能直接落地的开源印刷 ERP；其余可作 UI/流程参考。

---

## 二、⭐ 国产进销存+财务型 ERP（覆盖客户、订单、库存、财务，但生产工序流较薄）

| 项目 | ⭐ | 语言/栈 | 仓库 | 覆盖度 | 说明 |
|---|---|---|---|---|---|
| **jshERP（管伊佳ERP，原华夏ERP）** | 4528 | SpringBoot | [`jishenghua/jshERP`](https://github.com/jishenghua/jshERP) | ★★★★ 65% | 中文社区最活跃的进销存+财务开源ERP，**角色权限精细到按钮菜单**（与需求"多层权限隔离"高度契合），SaaS模式，模块齐备。**推荐**。 |
| **JSH_ERP** | 56 | SpringBoot | [`jiangyabo/JSH_ERP`](https://github.com/jiangyabo/JSH_ERP) | ★★★ 60% | 早期版本分支，功能与 jshERP 同源。 |
| **xingyun（星云ERP）** | 169 | SpringBoot | [`lframework/xingyun`](https://github.com/lframework/xingyun) | ★★★★ 65% | 星云ERP，中小企业完全开源，SpringBoot。 |
| **redragon-erp** | 368 | Java | [`redragon1985/redragon-erp`](https://github.com/redragon1985/redragon-erp) | ★★★ 55% | 小微企业 ERP，免费、稳定、灵活。 |
| **oms-erp（FJ-OMS）** | 1916 | SpringCloud/Istio | [`FJ-OMS/oms-erp`](https://github.com/FJ-OMS/oms-erp) | ★★★ 55% | 一站式全渠道业务中台，**OMS+WMS+财务**，微服务架构。 |
| **erp-pro（Skyeye云）** | 636 | SpringBoot+UniApp+AntDV | [`weizhiqiang1995/erp-pro`](https://github.com/weizhiqiang1995/erp-pro) | ★★★★ 70% | **零代码**，50+流程，含 CRM/PM/ERP/MES/ADM/OA/EHR/AI/商城/财务/考勤/薪资。模块多但偏"全家桶"。 |
| **itcloudy/ERP** | 826 | Go (beego) | [`itcloudy/ERP`](https://github.com/itcloudy/ERP) | ★★ 40% | Go 写的进销存，国产里较老牌。 |
| **okhelper** | 96 / 238 | Java + Vue | [`okhelperTeam/okhelper-service`](https://github.com/okhelperTeam/okhelper-service) / [`okhelper-web`](https://github.com/okhelperTeam/okhelper-web) | ★★ 40% | 云进销存（SaaS），前后端全家桶。 |
| **Discovery** | 627 | PHP (Dcat-admin) | [`youyingxiang/Discover`](https://github.com/youyingxiang/Discover) | ★★ 35% | 国产进销存。 |
| **chenbool/wms** | 357 | PHP | [`chenbool/wms`](https://github.com/chenbool/wms) | ★ 25% | PHP 仓库进销存。 |
| **EasyERP_open_source** | 237 | JS | [`EasyERP/EasyERP_open_source`](https://github.com/EasyERP/EasyERP_open_source) | ★★ 35% | 简易 ERP。 |

---

## 三、⭐⭐ 通用 ERP/MES 框架（工序流转/工位强，需要二次定制）

| 项目 | ⭐ | 语言/栈 | 仓库 | 覆盖度 | 说明 |
|---|---|---|---|---|---|
| **odoo（社区版）** | 53848 | Python+JS | [`odoo/odoo`](https://github.com/odoo/odoo) | ★★★★ 70% | 世界级开源 ERP，**Manufacturing 模块原生支持工位/工序流转/计件**，合同/库存/财务/HR 全覆盖；缺点是中文本地化和学校细分行业需深度定制。**强烈推荐评估**。 |
| **OCA/manufacture（Odoo 制造业插件）** | 270 | Python | [`OCA/manufacture`](https://github.com/OCA/manufacture) | — | Odoo 官方协会制造业模块集合，含条码/MRP/工序。 |
| **idurar-erp-crm** | 8692 | Node.js+React | [`idurar/idurar-erp-crm`](https://github.com/idurar/idurar-erp-crm) | ★★★ 50% | Node/React 全栈 ERP/CRM/会计/开票，**部署简单、现代技术栈**。 |
| **inoerp** | 839 | Go+Flutter | [`inoerp/inoerp`](https://github.com/inoerp/inoerp) | ★★★ 50% | OneApp 架构（Go后端+Flutter前端），企业管理套件。 |
| **metasfresh** | 2405 | Java | [`metasfresh/metasfresh`](https://github.com/metasfresh/metasfresh) | ★★★ 50% | 欧洲主流开源 ERP，强调快速灵活。 |
| **idempiere** | 655 | Java | [`idempiere/idempiere`](https://github.com/idempiere/idempiere) | ★★★ 50% | 全开源业务套件（ERP/CRM/MFG/SCM/POS）。 |
| **ERPNext / Frappe** | — | Python+JS | [`frappe/erpnext`](https://github.com/frappe/erpnext) | ★★★★ 70% | **与 Odoo 并列**，对学校/制造业/库存/HR 全覆盖；社区更轻量。 |
| **erpnext_china** | 79 | Python | [`saoxia/erpnext_china`](https://github.com/saoxia/erpnext_china) | ★★★ 55% | **ERPNext 中国本地化**，解决中文/中国会计准则。 |
| **smart_manufacturing（ERPNext 插件）** | 1 | Python | [`mohsinalimat/smart_manufacturing`](https://github.com/mohsinalimat/smart_manufacturing) | ★★★ 60% | ERPNext 智能制造套件，含车间作业、成本、MRP、追溯。 |
| **erpjs（iDempiere 微服务版）** | 119 | TS/JS | [`iDempiere-micro/erpjs`](https://github.com/iDempiere-micro/erpjs) | ★★ 40% | iDempiere 无头 ERP/CRM。 |
| **carbon（碳）** | 2377 | TS | [`crbnos/carbon`](https://github.com/crbnos/carbon) | ★★★★ 70% | **专为复杂装配/合同制造/MES/QMS 设计**，工序流转优秀。 |
| **ever-gauzy** | 4342 | TS/NestJS | [`ever-co/ever-gauzy`](https://github.com/ever-co/ever-gauzy) | ★★★ 55% | ERP/CRM/HRM/ATS/PM 全业务管理平台。 |
| **open-mercato** | 1663 | TS | [`open-mercato/open-mercato`](https://github.com/open-mercato/open-mercato) | ★★★ 55% | AI 工程化 CRM/ERP，多租户、RBAC、领域模块。 |
| **Viet-ERP** | 551 | TS | [`nclamvn/Viet-ERP`](https://github.com/nclamvn/Viet-ERP) | ★★ 40% | 越南 ERP，多语言可借鉴。 |
| **OpenConstructionERP** | 697 | Python | [`datadrivenconstruction/OpenConstructionERP`](https://github.com/datadrivenconstruction/OpenConstructionERP) | ★★ 35% | 建筑工程 ERP，BOQ/AI成本匹配，71 模块参考价值。 |
| **iota-sdk** | 459 | Go | [`iota-uz/iota-sdk`](https://github.com/iota-uz/iota-sdk) | ★★ 40% | 模块化 ERP（替代 SAP/Oracle/Odoo 的现代 UI）。 |
| **nocobase** | 23743 | TS/React | [`nocobase/nocobase`](https://github.com/nocobase/nocobase) | ★★★ 55% | **AI+无代码平台，可快速搭建业务系统**，对"工作量大的字段自定义"友好。 |
| **SPMS（智能生产管理）** | 300 | Java | [`s-pms/SPMS-Server`](https://github.com/s-pms/SPMS-Server) | ★★★★ 75% | **MES+WMS+ERP+QMS+IoT 一体化**，最贴合"工序流转+多仓库+车间计件"。**推荐重点评估**。 |
| **free-mes** | 400 | PLpgSQL | [`metaxk-company/free-mes`](https://github.com/metaxk-company/free-mes) | ★★★ 55% | 免费 MES。 |
| **WebVella ERP** | — | Stencil | [`WebVella/WebVella-ERP-StencilJs`](https://github.com/WebVella/WebVella-ERP-StencilJs) | ★★ 30% | Web组件化 ERP。 |
| **BlueSeer ERP** | 167 | Java | [`blueseerERP/blueseer`](https://github.com/blueseerERP/blueseer) | ★★ 35% | 制造业免费 ERP + EDI。 |
| **scipio-erp** | 370 | Java | [`ilscipio/scipio-erp`](https://github.com/ilscipio/scipio-erp) | ★★ 35% | 跨国电商+ERP框架。 |
| **Mini-ERP / SaaS 模板** | — | — | [`gonza8/Mini-ERP-Open-source`](https://github.com/gonza8/Mini-ERP-Open-source) / [`Boom-Vitt/boombignose-erp`](https://github.com/Boom-Vitt/boombignose-erp) | ★ 20% | 现代 Next.js + Supabase 的小 ERP 模板，可作前端脚手架。 |

---

## 四、⭐ 计件/工资/人事（人事模块补丁）

| 项目 | ⭐ | 语言/栈 | 仓库 | 覆盖度 | 说明 |
|---|---|---|---|---|---|
| **clothing-factory-app** | 1 | HTML | [`Elwinfan/clothing-factory-app`](https://github.com/Elwinfan/clothing-factory-app) | ★ 25% | 服装厂计件管理。 |
| **华新工厂计件工资管理 V1.0** | 1 | Vue | [`Qxue23/piece-wage-system`](https://github.com/Qxue23/piece-wage-system) | ★★ 35% | **计件工资管理系统**，可直接借鉴 UI/逻辑。 |
| **PRO_（微信小程序计件 SaaS）** | 0 | JS | [`ShayHarlen/-PRO_-`](https://github.com/ShayHarlen/-PRO_-) | ★★ 35% | 工厂计件 + 微信云开发 + ESP32 标签打印 + 二维码流转，**与需求"条码工序"高度一致**。 |
| **HRMS（Odoo/ERPNext 自带）** | — | — | — | — | 若选 Odoo/ERPNext，HR/工资/考勤模块原生。 |

---

## 五、⭐ 学校/教育细分 ERP（学校端角色体系可借鉴）

| 项目 | ⭐ | 语言/栈 | 仓库 | 覆盖度 | 说明 |
|---|---|---|---|---|---|
| **College-ERP** | 184 | Node/Express/Mongo | [`Ansarimajid/College-ERP`](https://github.com/Ansarimajid/College-ERP) | ★★ 35% | 学校 ERP，校长/组长/教师分层参考。 |
| **biprodas/school-erp** | 49 | TS | [`biprodas/school-erp`](https://github.com/biprodas/school-erp) | ★★ 35% | 学校管理（学籍/考勤/费用/考试）。 |
| **Gaurav-Verma07/school-erp-system** | 9 | — | [`Gaurav-Verma07/school-erp-system`](https://github.com/Gaurav-Verma07/school-erp-system) | ★ 20% | 学校 ERP。 |
| **FusionIIIT** | 15 | — | [`Velle-log/FusionIIIT`](https://github.com/Velle-log/FusionIIIT) | ★ 25% | 高校 ERP（IIITDM Jabalpur）。 |
| **SchoolERP-API** | 35 | — | [`stoic1979/SchoolERP-API`](https://github.com/stoic1979/SchoolERP-API) | ★ 25% | 学校 ERP API。 |
| **bippo/openbravo** | 79 | — | [`bippo/openbravo`](https://github.com/bippo/openbravo) | ★★ 30% | Openbravo（已被官仓取代，但旧版可看）。 |

> **注意**：这些都是"教育管理"（学籍/课程），并非"印刷订单"。但**校外驻点 + 多层级账号（后勤校长/课题组长/教师/学生）的权限模型**可直接借鉴。

---

## 六、⭐⭐ 最终建议组合（最少定制工作量）

按需求覆盖度从高到低，给出五种"开源底座 + 二次开发"路径：

| 方案 | 底座 | 二次开发重点 | 预估覆盖度 |
|---|---|---|---|
| **A. 印刷专用底座（最省力）** | `jiumierp`（小象智慧ERP） | ① 客户合同额度模块二次开发；② 微信小程序/Web客户端；③ PC端工位扫码工序；④ 数据隔离加固；⑤ 校外驻点简化版 | **可达 80%+** |
| **B. 通用 ERP+中文本地化（最稳）** | `jshERP`（管伊佳） + `SPMS-Server`（生产MES） | ① 印刷工序自定义（印刷→切纸→装订→打包→运输→签收）；② 客户合同分项单价；③ 驻点分仓；④ 客户小程序 | **可达 70%+** |
| **C. 国际化大平台（最灵活）** | `odoo/odoo`（社区版） + `OCA/manufacture` + `erpnext_china`（备选ERPNext） | ① 印刷行业字段自定义；② 学校细分角色；③ 微信小程序对接；④ 数据隔离通过 record rule 实现 | **可达 75%+** |
| **D. 现代 TypeScript 全栈** | `idurar/idurar-erp-crm` 或 `crbnos/carbon`（MES） | 工序流转现成，但中文/印刷行业字段需新建 | **可达 60-70%** |
| **E. 零代码快速验证** | `nocobase` 或 `weizhiqiang1995/erp-pro`（Skyeye） | 拖拽搭建七大模块；后期再选择性重写 | **可达 50-60%（MVP验证快）** |

---

## 七、调研报告下一步建议

1. **克隆某个仓库到 `/home/pine/workspace/github/`** 做本地深度分析（推荐先克隆 `jiumierp`、`jshERP`、`SPMS-Server`、`idurar-erp-crm` 四个对比）；
2. 对某个仓库生成 **README/架构/技术栈摘要**；
3. 输出 **模块覆盖矩阵表**（七大模块 × 各候选仓库）；
4. 输出 **二次开发工作量估算**（按 A/B/C/D 方案分别估算）。

---

## 附录：检索记录

| 关键词 | 结果数 | 备注 |
|---|---|---|
| `erp` (Java) | 30+ | 包含 jshERP、oms-erp、metasfresh、idempiere、xingyun 等 |
| `erp` (Go) | 30+ | itcloudy/ERP、iota-sdk 等 |
| `erp` (JavaScript/TypeScript) | 60+ | idurar、inoerp、grocy、nocobase、carbon、ever-gauzy 等 |
| `manufacturing ERP` | 25 | 大多是简单毕业设计/小项目 |
| `MES manufacturing` | 25 | SPMS、free-mes、Nature924 MES 等 |
| `odoo` | 20+ | 53k+ stars 的 odoo/odoo 是事实标准 |
| `ERPNext frappe` | 15 | 包含 erpnext_china 本地化 |
| `印刷 ERP` / `印刷管理` | 10+ | **jiumierp 是最对口的中文印刷ERP** |
| `work order routing` | 5 | 偏向车间 MES 概念 |
| `进销存` | 20+ | 国产进销存大杂烩 |
| `工厂 计件` | 3 | 服装厂、华新工厂计件系统、微信小程序计件SaaS |
| `工单 工序` / `scm wip` / `production routing job shop` | 0 | GitHub 中文结果稀薄 |
| `erp open source` | 20 | 含 EasyERP_open_source 等小型项目 |
| `school ERP / college-erp` | 6 | 教育细分，仅供角色权限模型参考 |

合计约 **300+ 个仓库** 已纳入筛选，最终候选清单保留 **50+ 个有效项目**。