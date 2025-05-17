# Logistics Management System (LMS) 🚚

an app designed for the manangement of logistic corporations.


It all comes from a thought from one of our friends that he needs an app/website to help him to optimise the management of a logistic corporation owned by his father.
In this project, we are trying to build an application that is user-oriented, versatile, and easy-to-use.




[![React Version](https://img.shields.io/badge/react-18.2.0-blue)](https://react.dev/)
[![Spring Boot Version](https://img.shields.io/badge/spring_boot-3.1.5-green)](https://spring.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**基于物联网的智能物流管理解决方案** - 专为中小型物流企业设计的全流程数字化管理平台

![系统界面预览](docs/screenshots/dashboard-preview.png)

## 🌟 核心价值主张
通过数字化手段解决传统物流行业四大痛点：
1. **运力浪费** - 智能路线优化算法降低空驶率
2. **信息孤岛** - 全流程可视化追踪系统
3. **人工错误** - 自动化EDI数据对接
4. **成本失控** - 实时吨公里成本分析

## 🚀 功能全景
### 核心模块
| 模块 | 功能亮点 | 技术实现 |
|------|----------|----------|
| **运单管理** | 智能OCR识别托运单 | Tesseract+OpenCV |
| **仓储管理** | 3D库位可视化 | Three.js + WebGL |
| **车辆调度** | 动态路径规划 | OSRM引擎 + 遗传算法 |
| **成本分析** | 实时吨公里成本 | Apache Flink流处理 |
| **客户门户** | 微信小程序对接 | Taro框架 |

### 特色功能
- 📦 **智能称重扫描**：支持蓝牙电子秤和扫码枪协同工作
- 🌍 **多语言支持**：中文/英文语言包
- 📊 **BI看板**：可拖拽式数据可视化组件
- 📱 **混合部署**：支持公有云SaaS和私有化部署

## 🛠️ 技术架构
### 系统拓扑
```mermaid
graph TD
    A[移动端PDA] --> B(Spring Cloud Gateway)
    C[司机APP] --> B
    D[管理后台] --> B
    B --> E[认证中心]
    E --> F[运单服务]
    E --> G[仓储服务]
    E --> H[车辆服务]
    F --> I[PostgreSQL]
    G --> J[MongoDB]
    H --> K[Redis]
