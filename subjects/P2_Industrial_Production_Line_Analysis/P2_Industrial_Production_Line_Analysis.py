from mpi4py import MPI
import random

# 类型码全局解释字典 (生产线状态分析)
TYPE_DEF = {
    # 宏观生产效率分析 (A0-A2)
    'A0': '生产效率平衡',
    'A1': '生产速度过载',
    'A2': '人员设备滞后',
    'A3': '综合协调失衡',
    'A4': '设备产能比失衡',
    'A5': '综合效能不足',
    'A6': '能耗生产超标',

    # 质量能耗分析 (B0-B2)
    'B0': '质量能耗平衡',
    'B1': '能耗超标',
    'B2': '质量效率不匹配',
    'B3': '高速高耗模式',
    'B4': '生产能耗比例失调',
    'B5': '综合指标超标',

    # 人员设备协调分析 (C0-C2)
    'C0': '人员设备协调',
    'C1': '人员效率超载',
    'C2': '生产协调能力不足',
    'C3': '质量生产耦合异常',
    'C4': '质量人员能耗失配',
    'C5': '生产周期协调异常',
    'C6': '人员效率超载',
    'C7': '能耗人员比例过低',

    # 生产优化分析 (D0-D2)
    'D0': '生产优化平衡',
    'D1': '人均能耗异常',
    'D2': '综合需求过载',
    'D3': '设备功率失调',
    'D4': '设备承载不足',
}


def mpi_factory_analysis():
    """MPI并行工厂生产线分析处理函数"""
    # 初始化MPI通信环境
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    status = MPI.Status()

    # 存储结果的全局变量
    production_data = None
    analysis_results = []

    if rank == 0:
        # 主进程：负责数据生成、分发和宏观效率分析

        # 1. 随机生成五个核心生产线变量
        x = random.randint(50, 500)   # 生产速度 (件/小时)
        y = random.randint(70, 100)   # 质量指标 (%)
        z = random.randint(100, 1000) # 能耗 (kW)
        w = random.randint(60, 120)   # 人员效率 (%)
        m = random.randint(1, 10)     # 设备状态评分 (1-10分)

        # 存储数据供main函数访问
        production_data = [x, y, z, w, m]

        # 2. 分发数据到其他进程
        # 发给进程1：x, y, z (质量能耗分析)
        comm.send(x, dest=1, tag=1)
        comm.send(y, dest=1, tag=2)
        comm.send(z, dest=1, tag=3)

        # 发给进程2：y, z, w (人员设备协调分析)
        comm.send(y, dest=2, tag=1)
        comm.send(z, dest=2, tag=2)
        comm.send(w, dest=2, tag=3)

        # 发给进程3：z, w, m (生产优化分析)
        comm.send(z, dest=3, tag=1)
        comm.send(w, dest=3, tag=2)
        comm.send(m, dest=3, tag=3)

        # 3. 执行宏观生产效率分析 (xyzwm)
        type_code = 'A0'  # 默认为效率平衡状态
        analysis_detail = ""

        # 条件判断1: if x * 3 > y + z / 10 (生产速度过快，超出质量和能耗的合理配比)
        if x * 3 > y + z / 10:
            type_code = 'A1'
            production_intensity = x * 3
            quality_energy_ratio = y + z / 10
            speed_excess = production_intensity - quality_energy_ratio
            overload_factor = production_intensity / quality_energy_ratio if quality_energy_ratio > 0 else float('inf')
            production_stress = min(overload_factor * 25, 100)
            analysis_detail = f"生产过载分析: 生产强度={production_intensity:.1f}, 质量能耗配比={quality_energy_ratio:.1f}, 速度超量={speed_excess:.1f}, 过载因子={overload_factor:.2f}, 生产应力={production_stress:.1f}%"

        # 条件判断2: if w + m * 10 < x / 5 (人员效率和设备状态跟不上生产需求)
        if w + m * 10 < x / 5:
            type_code = 'A2'
            personnel_equipment_capacity = w + m * 10
            production_requirement = x / 5
            capacity_deficit = production_requirement - personnel_equipment_capacity
            lag_ratio = capacity_deficit / personnel_equipment_capacity if personnel_equipment_capacity > 0 else float('inf')
            system_lag_level = min(lag_ratio * 30, 95)
            analysis_detail = f"人员设备滞后分析: 人员设备容量={personnel_equipment_capacity:.1f}, 生产需求={production_requirement:.1f}, 容量缺口={capacity_deficit:.1f}, 滞后比={lag_ratio:.2f}, 系统滞后水平={system_lag_level:.1f}%"

        # 条件判断3: if y * w < x * m + 5000 (质量与人员效率的乘积低于生产与设备的协调值)
        if y * w < x * m + 5000:
            type_code = 'A3'
            quality_personnel_product = y * w
            production_equipment_coordination = x * m + 5000
            coordination_gap = production_equipment_coordination - quality_personnel_product
            imbalance_factor = coordination_gap / quality_personnel_product if quality_personnel_product > 0 else float('inf')
            coordination_stress = min(imbalance_factor * 18, 95)
            analysis_detail = f"综合协调失衡分析: 质量人员乘积={quality_personnel_product}, 生产设备协调值={production_equipment_coordination}, 协调缺口={coordination_gap:.1f}, 失衡因子={imbalance_factor:.2f}, 协调应力={coordination_stress:.1f}%"
        # 条件判断4: A4
        if x / (m + 1) > y + z / 50:
            type_code = 'A4'
            equipment_capacity_ratio = x / (m + 1)
            capacity_imbalance = (x / (m + 1)) - (y + z / 50)
            analysis_detail = f"设备产能比失衡分析: 设备产能比={equipment_capacity_ratio:.1f}, 质量能耗基准={y + z / 50:.1f}, 失衡量={capacity_imbalance:.1f}, 失衡度={min(capacity_imbalance * 0.8, 95):.1f}%"

        # 条件判断5: A5
        if (w + m * 8) ** 2 < x * y:
            type_code = 'A5'
            personnel_equipment_squared = (w + m * 8) ** 2
            comprehensive_efficiency_deficit = (x * y) - personnel_equipment_squared
            analysis_detail = f"综合效能不足分析: 人员设备平方={(w + m * 8) ** 2:.1f}, 生产质量积={x * y:.1f}, 效能缺口={comprehensive_efficiency_deficit:.1f}, 不足度={min(comprehensive_efficiency_deficit * 0.02, 95):.1f}%"

        # 条件判断6: A6
        if z / 5 + x > y * 2 + w:
            type_code = 'A6'
            energy_production_sum = z / 5 + x
            energy_production_excess = (z / 5 + x) - (y * 2 + w)
            analysis_detail = f"能耗生产超标分析: 能耗生产和={energy_production_sum:.1f}, 质量人员基准={y * 2 + w:.1f}, 超标量={energy_production_excess:.1f}, 超标度={min(energy_production_excess * 0.5, 95):.1f}%"

        # 4. 收集其他进程的分析结果
        quality_energy_result = comm.recv(source=1, tag=100, status=status)
        personnel_equipment_result = comm.recv(source=2, tag=200, status=status)
        optimization_result = comm.recv(source=3, tag=300, status=status)

        # 5. 组装完整结果
        analysis_results = [
            f"宏观生产效率 (xyzwm): {type_code} -> {TYPE_DEF.get(type_code, '未知')} | {analysis_detail}",
            f"质量能耗平衡 (xyz): {quality_energy_result['code']} -> {TYPE_DEF.get(quality_energy_result['code'], '未知')} | {quality_energy_result['detail']}",
            f"人员设备协调 (yzw): {personnel_equipment_result['code']} -> {TYPE_DEF.get(personnel_equipment_result['code'], '未知')} | {personnel_equipment_result['detail']}",
            f"生产优化分析 (zwm): {optimization_result['code']} -> {TYPE_DEF.get(optimization_result['code'], '未知')} | {optimization_result['detail']}"
        ]

        return production_data, analysis_results


    elif rank == 1:
        # 进程1：接收 x, y, z 进行质量能耗分析
        x = comm.recv(source=0, tag=1, status=status)
        y = comm.recv(source=0, tag=2, status=status)
        z = comm.recv(source=0, tag=3, status=status)

        type_code = 'B0'  # 默认为质量能耗平衡
        analysis_detail = ""

        # 条件判断4: if z > x * y / 30 + 200 (能耗超出按生产速度和质量应有的合理水平)
        if z > x * y / 30 + 200:
            type_code = 'B1'
            actual_energy = z
            expected_energy_level = x * y / 30 + 200
            energy_excess = actual_energy - expected_energy_level
            energy_waste_ratio = energy_excess / expected_energy_level if expected_energy_level > 0 else float('inf')
            energy_efficiency_loss = min(energy_waste_ratio * 28, 95)
            analysis_detail = f"能耗超标分析: 实际能耗={actual_energy}kW, 预期能耗水平={expected_energy_level:.1f}kW, 能耗超量={energy_excess:.1f}kW, 能耗浪费比={energy_waste_ratio:.2f}, 能效损失={energy_efficiency_loss:.1f}%"

        # 条件判断5: if x * z > y ** 2 * 15 (生产能耗乘积超出质量平方的倍数阈值)
        if x * z > y ** 2 * 15:
            type_code = 'B2'
            production_energy_product = x * z
            quality_squared_threshold = y ** 2 * 15
            multiplicative_excess = production_energy_product - quality_squared_threshold
            intensity_amplification_ratio = production_energy_product / quality_squared_threshold if quality_squared_threshold > 0 else float('inf')
            quality_intensity_mismatch = min(intensity_amplification_ratio * 20, 95)
            analysis_detail = f"质量强度失配分析: 生产能耗乘积={production_energy_product}, 质量平方阈值={quality_squared_threshold:.1f}, 乘积超量={multiplicative_excess:.1f}, 强度放大比={intensity_amplification_ratio:.2f}, 质量强度失配度={quality_intensity_mismatch:.1f}%"

        # 条件判断6: if x > (y - 50) * 4 and z > 600 (高速生产时质量调整后仍能耗过高)
        if x > (y - 50) * 4 and z > 600:
            type_code = 'B3'
            production_speed = x
            quality_adjusted_threshold = (y - 50) * 4
            high_energy_consumption = z
            speed_over_threshold = production_speed - quality_adjusted_threshold
            energy_intensity_factor = z / x if x > 0 else 0
            high_speed_sustainability = 100 - min(speed_over_threshold / 12 + energy_intensity_factor / 6, 88)
            analysis_detail = f"高速高耗分析: 生产速度={production_speed}件/h, 质量调整阈值={quality_adjusted_threshold:.1f}件/h, 高能耗={high_energy_consumption}kW, 速度超阈值={speed_over_threshold:.1f}件/h, 能耗强度因子={energy_intensity_factor:.2f}, 高速可持续性={high_speed_sustainability:.1f}%"
        # 条件判断7: B4
        if x ** 2 / 100 > y * z / 20:
            type_code = 'B4'
            production_squared = x ** 2 / 100
            production_energy_ratio_imbalance = (x ** 2 / 100) - (y * z / 20)
            analysis_detail = f"生产能耗比例失调分析: 生产平方值={production_squared:.1f}, 质量能耗积={y * z / 20:.1f}, 比例失调量={production_energy_ratio_imbalance:.1f}, 失调度={min(production_energy_ratio_imbalance * 0.3, 95):.1f}%"

        # 条件判断8: B5
        if (x + y) / 2 > z / 3 + 150:
            type_code = 'B5'
            production_quality_average = (x + y) / 2
            comprehensive_index_excess = ((x + y) / 2) - (z / 3 + 150)
            analysis_detail = f"综合指标超标分析: 生产质量均值={production_quality_average:.1f}, 能耗基准={z / 3 + 150:.1f}, 超标量={comprehensive_index_excess:.1f}, 超标度={min(comprehensive_index_excess * 0.6, 95):.1f}%"

        # 发送分析结果回主进程
        result = {'code': type_code, 'detail': analysis_detail}
        comm.send(result, dest=0, tag=100)


    elif rank == 2:
        # 进程2：接收 y, z, w 进行人员设备协调分析
        y = comm.recv(source=0, tag=1, status=status)
        z = comm.recv(source=0, tag=2, status=status)
        w = comm.recv(source=0, tag=3, status=status)

        type_code = 'C0'  # 默认为人员设备协调
        analysis_detail = ""

        # 条件判断7: if w / y > z / 120 (人员效率质量比值超出能耗比值标准)
        if w / y > z / 120:
            type_code = 'C1'
            personnel_quality_ratio = w / y if y > 0 else 0
            energy_ratio_standard = z / 120
            ratio_excess = personnel_quality_ratio - energy_ratio_standard
            ratio_imbalance_factor = ratio_excess / energy_ratio_standard if energy_ratio_standard > 0 else float('inf')
            personnel_efficiency_overload = min(ratio_imbalance_factor * 40, 95)
            analysis_detail = f"人员效率超载分析: 人员质量比值={personnel_quality_ratio:.2f}, 能耗比值标准={energy_ratio_standard:.2f}, 比值超量={ratio_excess:.2f}, 比值失衡因子={ratio_imbalance_factor:.2f}, 人员效率过载度={personnel_efficiency_overload:.1f}%"

        # 条件判断8: if y ** 2 + w ** 2 > z * 4 (质量人员平方和超出能耗的四倍阈值)
        if y ** 2 + w ** 2 > z * 4:
            type_code = 'C2'
            quality_personnel_square_sum = y ** 2 + w ** 2
            energy_quadruple_threshold = z * 4
            square_sum_excess = quality_personnel_square_sum - energy_quadruple_threshold
            quadratic_energy_imbalance = square_sum_excess / energy_quadruple_threshold if energy_quadruple_threshold > 0 else float('inf')
            coordination_quadratic_overload = min(quadratic_energy_imbalance * 25, 95)
            analysis_detail = f"生产协调能力不足分析: 质量人员平方和={quality_personnel_square_sum}, 能耗四倍阈值={energy_quadruple_threshold}, 平方和超量={square_sum_excess:.1f}, 二次能耗失衡度={quadratic_energy_imbalance:.2f}, 协调二次过载度={coordination_quadratic_overload:.1f}%"

        # 条件判断9: if w * z > y * 35 + 2800 (人员能耗乘积超出质量倍数基准)
        if w * z > y * 35 + 2800:
            type_code = 'C3'
            personnel_energy_product = w * z
            quality_multiple_baseline = y * 35 + 2800
            multiplicative_overload = personnel_energy_product - quality_multiple_baseline
            cross_factor_imbalance = multiplicative_overload / quality_multiple_baseline if quality_multiple_baseline > 0 else float('inf')
            personnel_energy_dominance = min(cross_factor_imbalance * 18, 95)
            analysis_detail = f"质量生产耦合异常分析: 人员能耗乘积={personnel_energy_product}, 质量倍数基准={quality_multiple_baseline:.1f}, 乘积过载量={multiplicative_overload:.1f}, 交叉因子失衡度={cross_factor_imbalance:.2f}, 人员能耗主导度={personnel_energy_dominance:.1f}%"
        # 条件判断10: C4
        if y * w / 100 > z / 8 + 50:
            type_code = 'C4'
            quality_personnel_ratio = y * w / 100
            quality_personnel_energy_mismatch = (y * w / 100) - (z / 8 + 50)
            analysis_detail = f"质量人员能耗失配分析: 质量人员比={quality_personnel_ratio:.1f}, 能耗基准={z / 8 + 50:.1f}, 失配量={quality_personnel_energy_mismatch:.1f}, 失配度={min(quality_personnel_energy_mismatch * 1.5, 95):.1f}%"

        # 条件判断11: C5
        if (y + z / 10) % 20 < w / 10:
            type_code = 'C5'
            quality_energy_remainder = (y + z / 10) % 20
            production_cycle_coordination_anomaly = (w / 10) - ((y + z / 10) % 20)
            analysis_detail = f"生产周期协调异常分析: 质量能耗余数={quality_energy_remainder:.1f}, 人员基准={w / 10:.1f}, 协调差={production_cycle_coordination_anomaly:.1f}, 异常度={min(production_cycle_coordination_anomaly * 8, 95):.1f}%"

        # 条件判断12: C6
        if w ** 2 / 50 > y + z / 15:
            type_code = 'C6'
            personnel_squared = w ** 2 / 50
            personnel_efficiency_overload = (w ** 2 / 50) - (y + z / 15)
            analysis_detail = f"人员效率超载分析: 人员平方值={personnel_squared:.1f}, 质量能耗和={y + z / 15:.1f}, 超载量={personnel_efficiency_overload:.1f}, 超载度={min(personnel_efficiency_overload * 1.2, 95):.1f}%"

        # 条件判断13: C7
        if z / (w + 1) < y / 2 - 20:
            type_code = 'C7'
            energy_personnel_ratio = z / (w + 1)
            energy_personnel_ratio_deficiency = (y / 2 - 20) - (z / (w + 1))
            analysis_detail = f"能耗人员比例过低分析: 能耗人员比={energy_personnel_ratio:.2f}, 质量基准={y / 2 - 20:.1f}, 比例缺口={energy_personnel_ratio_deficiency:.1f}, 过低度={min(energy_personnel_ratio_deficiency * 2, 95):.1f}%"
        # 发送分析结果回主进程
        result = {'code': type_code, 'detail': analysis_detail}
        comm.send(result, dest=0, tag=200)


    elif rank == 3:
        # 进程3：接收 z, w, m 进行生产优化分析
        z = comm.recv(source=0, tag=1, status=status)
        w = comm.recv(source=0, tag=2, status=status)
        m = comm.recv(source=0, tag=3, status=status)

        type_code = 'D0'  # 默认为生产优化平衡
        analysis_detail = ""

        # 条件判断10: if z * m < w * 20 (能耗设备乘积低于人员效率的倍数阈值)
        if z * m < w * 20:
            type_code = 'D1'
            energy_equipment_product = z * m
            personnel_efficiency_multiple = w * 20
            multiplicative_deficit = personnel_efficiency_multiple - energy_equipment_product
            cross_multiplication_imbalance = multiplicative_deficit / energy_equipment_product if energy_equipment_product > 0 else float('inf')
            energy_equipment_underutilization = min(cross_multiplication_imbalance * 25, 95)
            analysis_detail = f"人均能耗异常分析: 能耗设备乘积={energy_equipment_product}, 人员效率倍数={personnel_efficiency_multiple}, 乘积缺口={multiplicative_deficit:.1f}, 交叉乘积失衡度={cross_multiplication_imbalance:.2f}, 能耗设备利用不足度={energy_equipment_underutilization:.1f}%"

        # 条件判断11: if z + w * 2 > m * 45 + 1200 (能耗人员需求超出设备综合支撑能力)
        if z + w * 2 > m * 45 + 1200:
            type_code = 'D2'
            energy_personnel_demand = z + w * 2
            equipment_comprehensive_support = m * 45 + 1200
            demand_overload = energy_personnel_demand - equipment_comprehensive_support
            comprehensive_overload_ratio = demand_overload / equipment_comprehensive_support if equipment_comprehensive_support > 0 else float('inf')
            comprehensive_demand_overload = min(comprehensive_overload_ratio * 24, 95)
            analysis_detail = f"综合需求过载分析: 能耗人员需求={energy_personnel_demand:.1f}, 设备综合支撑={equipment_comprehensive_support:.1f}, 需求过载量={demand_overload:.1f}, 综合过载比={comprehensive_overload_ratio:.2f}, 综合需求过载度={comprehensive_demand_overload:.1f}%"

        # 条件判断12: if z % (m + 1) == 0 and w > 85 (能耗被设备档位整除且人员高效率的异常匹配)
        if z % (m + 1) == 0 and w > 85:
            type_code = 'D3'
            energy_consumption = z
            equipment_tier = m + 1
            personnel_efficiency = w
            perfect_divisibility_factor = z // equipment_tier
            high_efficiency_threshold = 85
            efficiency_excess = w - high_efficiency_threshold
            anomalous_perfect_match_level = min(perfect_divisibility_factor / 20 + efficiency_excess, 95)
            analysis_detail = f"设备功率失调分析: 能耗={energy_consumption}kW, 设备档位={equipment_tier}, 完美整除因子={perfect_divisibility_factor}, 人员效率={personnel_efficiency}%, 高效率阈值={high_efficiency_threshold}%, 异常完美匹配度={anomalous_perfect_match_level:.1f}%"
        # 条件判断13: D4
        if (z + w * 3) / 2 < m ** 2 * 15:
            type_code = 'D4'
            energy_personnel_average = (z + w * 3) / 2
            equipment_capacity_shortage = (m ** 2 * 15) - ((z + w * 3) / 2)
            analysis_detail = f"设备承载不足分析: 能耗人员均值={energy_personnel_average:.1f}, 设备容量={m ** 2 * 15:.1f}, 承载缺口={equipment_capacity_shortage:.1f}, 不足度={min(equipment_capacity_shortage * 0.15, 95):.1f}%"

        # 发送分析结果回主进程
        result = {'code': type_code, 'detail': analysis_detail}
        comm.send(result, dest=0, tag=300)

    # 非主进程返回None
    return None, None


def main():
    """主控制函数：数据生成和结果输出"""
    # 获取MPI rank
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    # 调用MPI分析函数
    production_data, analysis_results = mpi_factory_analysis()

    # 只在主进程中进行输出
    if rank == 0 and production_data is not None:
        x, y, z, w, m = production_data

        print("=" * 70)
        print("  工厂生产线监控系统 - MPI并行计算版本  ")
        print("=" * 70)
        print()

        print("--- 实时生产线数据 ---")
        print(f"生产速度(X): {x} 件/小时")
        print(f"质量指标(Y): {y}%")
        print(f"能耗(Z): {z} kW")
        print(f"人员效率(W): {w}%")
        print(f"设备状态(M): {m} 分")
        print()

        print("--- 生产线综合分析报告 ---")
        for i, result in enumerate(analysis_results, 1):
            print(f"{i}. {result}")
        print()

        print("=" * 70)
        print("MPI并行分析完成 - 4个进程同时工作")
        print("=" * 70)


if __name__ == "__main__":
    main()