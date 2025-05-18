-- 创建货物信息主表
CREATE TABLE goods (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),  -- 唯一标识
    name VARCHAR(255) NOT NULL,                     -- 货品名称
    manufacturer VARCHAR(255),                      -- 生产厂家
    quantity INT CHECK (quantity > 0),              -- 件数（必须>0）
    volume DECIMAL(10,2) GENERATED ALWAYS AS (      -- 自动计算体积（立方米）
        COALESCE(length * width * height, NULL)
    ) STORED,
    tonnage DECIMAL(10,2) CHECK (tonnage >= 0),     -- 吨位（允许0）
    remark TEXT,                                     -- 备注信息
    created_at TIMESTAMPTZ DEFAULT NOW(),           -- 记录时间
    updated_at TIMESTAMPTZ DEFAULT NOW(),           -- 最后更新时间
    
    -- 尺寸测量（允许NULL，表示未测量）
    length DECIMAL(6,2) CHECK (length > 0),         -- 长度（米）
    width DECIMAL(6,2) CHECK (width > 0),           -- 宽度（米）
    height DECIMAL(6,2) CHECK (height > 0),         -- 高度（米）
    
    -- 复合约束
    CONSTRAINT valid_volume CHECK (
        (length IS NOT NULL AND width IS NOT NULL AND height IS NOT NULL) 
        OR volume IS NULL
    )
);

-- 创建索引优化查询
CREATE INDEX idx_goods_manufacturer ON goods(manufacturer);
CREATE INDEX idx_goods_created ON goods(created_at);

-- 插入示例数据
INSERT INTO goods (name, manufacturer, quantity, tonnage, length, width, height, remark) 
VALUES 
    ('钢板', '宝山钢铁', 50, 12.5, 2.4, 1.2, 0.05, '冷轧钢板-需防潮'),
    ('机电设备', '三一重工', 3, NULL, 3.0, 2.0, 1.8, '精密仪器-禁止倒置'),
    ('化工原料', '万华化学', 200, 8.0, NULL, NULL, NULL, '液体桶装-需恒温存储');

-- 验证自动计算的体积
SELECT name, volume FROM goods WHERE volume IS NOT NULL;