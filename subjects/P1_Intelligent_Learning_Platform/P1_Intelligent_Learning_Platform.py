from mpi4py import MPI
import random

# 类型码全局解释字典 (学习平台状态分析)
TYPE_DEF = {
    # 宏观学习效能分析 (A0-A3)
    'A0': '学习效能平衡',
    'A1': '学习进度过激',
    'A2': '互动平台滞后',
    'A3': '综合学习失衡',
    'A4': '学习效能协同不足',
    'A5': '时长资源分配失衡',
    'A6': '平台进度匹配异常',
    'A7': '学习响应过度活跃',

    # 知识时长平衡分析 (B0-B3)
    'B0': '知识时长平衡',
    'B1': '时长投入过度',
    'B2': '知识进度失配',
    'B3': '高进度低效模式',
    'B4': '进度膨胀效应',
    'B5': '知识掌握度偏移',
    'B6': '时长周期波动',

    # 互动参与协调分析 (C0-C3)
    'C0': '互动参与协调',
    'C1': '互动参与过载',
    'C2': '学习协调不足',
    'C3': '知识参与耦合异常',
    'C4': '掌握度参与失配',
    'C5': '学习周期同步异常',
    'C6': '互动强度超载',
    'C7': '时长参与比例失调',

    # 平台优化分析 (D0-D3)
    'D0': '平台优化平衡',
    'D1': '时长适配异常',
    'D2': '综合学习需求过载',
    'D3': '平台匹配失调',
    'D4': '平台承载力不足',
}


def mpi_learning_analysis():
    """MPI并行智能学习平台分析处理函数"""
    # 初始化MPI通信环境
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    status = MPI.Status()
    # 存储结果的全局变量
    learning_data = None
    analysis_results = []

    if rank == 0:
        # 主进程：负责数据生成、分发和宏观学习效能分析

        # 1. 随机生成五个核心学习平台变量
        x = random.randint(10, 100)   # 学习进度 (%)
        y = random.randint(40, 100)   # 知识掌握度 (%)
        z = random.randint(30, 300)   # 学习时长 (分钟/天)
        w = random.randint(20, 100)   # 互动参与度 (%)
        m = random.randint(1, 10)     # 平台适配度 (1-10分)

        # 存储数据供main函数访问
        learning_data = [x, y, z, w, m]
        # 发给进程1：x, y, z (知识时长平衡分析)
        comm.send(x, dest=1, tag=1)
        comm.send(y, dest=1, tag=2)
        comm.send(z, dest=1, tag=3)

        # 发给进程2：y, z, w (互动参与协调分析)
        comm.send(y, dest=2, tag=1)
        comm.send(z, dest=2, tag=2)
        comm.send(w, dest=2, tag=3)

        # 发给进程3：z, w, m (平台优化分析)
        comm.send(z, dest=3, tag=1)
        comm.send(w, dest=3, tag=2)
        comm.send(m, dest=3, tag=3)

        # 3. 执行宏观学习效能分析 (xyzwm)
        type_code = 'A0'  # 默认为学习效能平衡状态
        analysis_detail = ""

        # 条件判断1: if x + y > z / 5 + w * 2 (进度掌握度和超出时长分配与互动倍数的平衡)
        if x + y > z / 5 + w * 2:
            type_code = 'A1'
            progress_mastery_total = x + y
            time_interaction_allocation = z / 5 + w * 2
            learning_capacity_overflow = progress_mastery_total - time_interaction_allocation
            resource_utilization_ratio = progress_mastery_total / time_interaction_allocation if time_interaction_allocation > 0 else float('inf')
            learning_intensity_pressure = min(resource_utilization_ratio * 18, 100)
            analysis_detail = f"学习强度过激分析: 进度掌握总和={progress_mastery_total:.1f}, 时长互动配置={time_interaction_allocation:.1f}, 学习容量溢出={learning_capacity_overflow:.1f}, 资源利用比={resource_utilization_ratio:.2f}, 学习强度压力={learning_intensity_pressure:.1f}%"

        # 条件判断2: if m ** 2 > x / 4 + y / 6 (平台适配度平方超出进度掌握度的分数配比)
        if m ** 2 > x / 4 + y / 6:
            type_code = 'A2'
            platform_adaptation_squared = m ** 2
            progress_mastery_fraction_sum = x / 4 + y / 6
            adaptation_dominance_excess = platform_adaptation_squared - progress_mastery_fraction_sum
            platform_over_optimization = adaptation_dominance_excess / progress_mastery_fraction_sum if progress_mastery_fraction_sum > 0 else float('inf')
            learning_platform_mismatch = min(platform_over_optimization * 28, 95)
            analysis_detail = f"平台过度优化分析: 平台适配平方={platform_adaptation_squared:.1f}, 进度掌握分数和={progress_mastery_fraction_sum:.1f}, 适配主导超量={adaptation_dominance_excess:.1f}, 平台过度优化比={platform_over_optimization:.2f}, 学习平台失配度={learning_platform_mismatch:.1f}%"

        # 条件判断3: if (x + w) / 2 < y - m * 8 (进度互动平均值低于掌握度减去平台倍数)
        if (x + w) / 2 < y - m * 8:
            type_code = 'A3'
            progress_interaction_average = (x + w) / 2
            mastery_platform_adjustment = y - m * 8
            engagement_deficit = mastery_platform_adjustment - progress_interaction_average
            learning_engagement_gap_ratio = engagement_deficit / progress_interaction_average if progress_interaction_average > 0 else float('inf')
            comprehensive_engagement_lag = min(learning_engagement_gap_ratio * 24, 95)
            analysis_detail = f"学习参与滞后分析: 进度互动平均={progress_interaction_average:.1f}, 掌握度平台调整={mastery_platform_adjustment:.1f}, 参与缺口={engagement_deficit:.1f}, 学习参与缺口比={learning_engagement_gap_ratio:.2f}, 综合参与滞后度={comprehensive_engagement_lag:.1f}%"
        # 条件判断4: A4
        if (x * y) / 100 < w + m * 5:
            type_code = 'A4'
            synergy_deficit = (w + m * 5) - (x * y) / 100
            coordination_insufficiency = min(synergy_deficit * 2.5, 95)
            analysis_detail = f"学习效能协同不足分析: 进度掌握积={(x * y) / 100:.1f}, 互动平台配置={w + m * 5:.1f}, 协同缺口={synergy_deficit:.1f}, 协同不足度={coordination_insufficiency:.1f}%"

        # 条件判断5: A5
        if z - w * 2 > x + y / 3:
            type_code = 'A5'
            resource_allocation_gap = (z - w * 2) - (x + y / 3)
            time_resource_imbalance = min(resource_allocation_gap * 0.8, 95)
            analysis_detail = f"时长资源分配失衡分析: 时长互动差={z - w * 2:.1f}, 进度掌握和={x + y / 3:.1f}, 分配缺口={resource_allocation_gap:.1f}, 失衡度={time_resource_imbalance:.1f}%"

        # 条件判断6: A6
        if m * 10 + x > y + z / 4:
            type_code = 'A6'
            platform_progress_excess = (m * 10 + x) - (y + z / 4)
            matching_anomaly = min(platform_progress_excess * 1.2, 95)
            analysis_detail = f"平台进度匹配异常分析: 平台进度和={m * 10 + x:.1f}, 掌握时长和={y + z / 4:.1f}, 匹配超量={platform_progress_excess:.1f}, 异常度={matching_anomaly:.1f}%"

        # 条件判断7: A7
        if (w + y) / (x + 1) > z / 20 + m:
            type_code = 'A7'
            response_activity_ratio = (w + y) / (x + 1)
            learning_response_overactivity = min((response_activity_ratio - (z / 20 + m)) * 15, 95)
            analysis_detail = f"学习响应过度活跃分析: 互动掌握比={response_activity_ratio:.2f}, 时长平台基准={z / 20 + m:.2f}, 过度活跃度={learning_response_overactivity:.1f}%"

        # 4. 收集其他进程的分析结果
        knowledge_time_result = comm.recv(source=1, tag=100, status=status)
        interaction_participation_result = comm.recv(source=2, tag=200, status=status)
        platform_optimization_result = comm.recv(source=3, tag=300, status=status)

        # 5. 组装完整结果
        analysis_results = [
            f"宏观学习效能 (xyzwm): {type_code} -> {TYPE_DEF.get(type_code, '未知')} | {analysis_detail}",
            f"知识时长平衡 (xyz): {knowledge_time_result['code']} -> {TYPE_DEF.get(knowledge_time_result['code'], '未知')} | {knowledge_time_result['detail']}",
            f"互动参与协调 (yzw): {interaction_participation_result['code']} -> {TYPE_DEF.get(interaction_participation_result['code'], '未知')} | {interaction_participation_result['detail']}",
            f"平台优化分析 (zwm): {platform_optimization_result['code']} -> {TYPE_DEF.get(platform_optimization_result['code'], '未知')} | {platform_optimization_result['detail']}"
        ]

        return learning_data, analysis_results


    elif rank == 1:
        # 进程1：接收 x, y, z 进行知识时长平衡分析
        x = comm.recv(source=0, tag=1, status=status)
        y = comm.recv(source=0, tag=2, status=status)
        z = comm.recv(source=0, tag=3, status=status)

        type_code = 'B0'  # 默认为知识时长平衡
        analysis_detail = ""

        # 条件判断4: if x - y > z / 15 (学习进度减去掌握度超出时长的分数阈值)
        if x - y > z / 15:
            type_code = 'B1'
            progress_mastery_gap = x - y
            time_allocation_unit = z / 15
            learning_pace_imbalance = progress_mastery_gap - time_allocation_unit
            pace_acceleration_factor = progress_mastery_gap / time_allocation_unit if time_allocation_unit > 0 else float('inf')
            knowledge_absorption_lag = min(pace_acceleration_factor * 32, 95)
            analysis_detail = f"知识吸收滞后分析: 进度掌握差距={progress_mastery_gap:.1f}, 时长配置单元={time_allocation_unit:.1f}, 学习节奏失衡={learning_pace_imbalance:.1f}, 节奏加速因子={pace_acceleration_factor:.2f}, 知识吸收滞后度={knowledge_absorption_lag:.1f}%"

        # 条件判断5: if y / x > z / 40 (掌握度进度比值超出时长比值标准)
        if y / x > z / 40:
            type_code = 'B2'
            mastery_progress_efficiency = y / x if x > 0 else 0
            time_distribution_standard = z / 40
            efficiency_ratio_surplus = mastery_progress_efficiency - time_distribution_standard
            learning_efficiency_amplification = efficiency_ratio_surplus / time_distribution_standard if time_distribution_standard > 0 else float('inf')
            knowledge_consolidation_pressure = min(learning_efficiency_amplification * 26, 95)
            analysis_detail = f"知识巩固压力分析: 掌握进度效率比={mastery_progress_efficiency:.2f}, 时间分布标准={time_distribution_standard:.2f}, 效率比值盈余={efficiency_ratio_surplus:.2f}, 学习效率放大度={learning_efficiency_amplification:.2f}, 知识巩固压力={knowledge_consolidation_pressure:.1f}%"

        # 条件判断6: if x + z < y * 3 (进度时长和低于掌握度的三倍)
        if x + z < y * 3:
            type_code = 'B3'
            progress_time_investment = x + z
            mastery_triple_benchmark = y * 3
            learning_resource_shortage = mastery_triple_benchmark - progress_time_investment
            resource_adequacy_deficit = learning_resource_shortage / progress_time_investment if progress_time_investment > 0 else float('inf')
            learning_foundation_instability = min(resource_adequacy_deficit * 29, 95)
            analysis_detail = f"学习基础不稳分析: 进度时间投入={progress_time_investment:.1f}, 掌握度三倍基准={mastery_triple_benchmark:.1f}, 学习资源短缺={learning_resource_shortage:.1f}, 资源充足度缺口={resource_adequacy_deficit:.2f}, 学习基础不稳定度={learning_foundation_instability:.1f}%"
        # 条件判断7: B4
        if x ** 2 / 100 > y + z / 10:
            type_code = 'B4'
            progress_inflation = (x ** 2 / 100) - (y + z / 10)
            inflation_effect = min(progress_inflation * 1.5, 95)
            analysis_detail = f"进度膨胀效应分析: 进度平方值={x ** 2 / 100:.1f}, 掌握时长和={y + z / 10:.1f}, 膨胀量={progress_inflation:.1f}, 膨胀度={inflation_effect:.1f}%"

        # 条件判断8: B5
        if (x + y + z) / 3 < y * 1.5:
            type_code = 'B5'
            mastery_deviation = (y * 1.5) - ((x + y + z) / 3)
            knowledge_offset = min(mastery_deviation * 1.8, 95)
            analysis_detail = f"知识掌握度偏移分析: 三要素均值={(x + y + z) / 3:.1f}, 掌握度倍数={y * 1.5:.1f}, 偏移量={mastery_deviation:.1f}, 偏移度={knowledge_offset:.1f}%"

        # 条件判断9: B6
        if z % 50 > x - y / 2:
            type_code = 'B6'
            time_cycle_fluctuation = (z % 50) - (x - y / 2)
            cycle_volatility = min(time_cycle_fluctuation * 3, 95)
            analysis_detail = f"时长周期波动分析: 时长周期余数={z % 50:.1f}, 进度掌握差={x - y / 2:.1f}, 波动量={time_cycle_fluctuation:.1f}, 波动度={cycle_volatility:.1f}%"

        # 发送分析结果回主进程
        result = {'code': type_code, 'detail': analysis_detail}
        comm.send(result, dest=0, tag=100)


    elif rank == 2:
        # 进程2：接收 y, z, w 进行互动参与协调分析
        y = comm.recv(source=0, tag=1, status=status)
        z = comm.recv(source=0, tag=2, status=status)
        w = comm.recv(source=0, tag=3, status=status)

        type_code = 'C0'  # 默认为互动参与协调
        analysis_detail = ""

        # 条件判断7: if w ** 2 - y * z < 800 (参与度平方减去掌握度时长乘积低于800)
        if w ** 2 - y * z < 800:
            type_code = 'C1'
            participation_squared = w ** 2
            mastery_time_product = y * z
            interaction_energy_deficit = participation_squared - mastery_time_product
            minimum_threshold = 800
            energy_shortfall = minimum_threshold - interaction_energy_deficit
            participation_energy_insufficiency = energy_shortfall / minimum_threshold if minimum_threshold > 0 else 0
            participation_motivation_lag = min(participation_energy_insufficiency * 40, 95)
            analysis_detail = f"参与动力不足分析: 参与度平方={participation_squared}, 掌握时长积={mastery_time_product:.1f}, 互动能量缺口={interaction_energy_deficit:.1f}, 最低阈值={minimum_threshold}, 能量不足量={energy_shortfall:.1f}, 参与动力滞后度={participation_motivation_lag:.1f}%"

        # 条件判断8: if (y + w) % 25 > z / 12 (掌握度参与度和的模25余数超出时长的十二分之一)
        if (y + w) % 25 > z / 12:
            type_code = 'C2'
            mastery_participation_sum = y + w
            modular_remainder = (y + w) % 25
            time_fractional_threshold = z / 12
            modular_excess = modular_remainder - time_fractional_threshold
            cyclical_learning_imbalance = modular_excess / time_fractional_threshold if time_fractional_threshold > 0 else float('inf')
            learning_rhythm_disruption = min(cyclical_learning_imbalance * 35, 95)
            analysis_detail = f"学习周期紊乱分析: 掌握参与和={mastery_participation_sum}, 模运算余数={modular_remainder:.1f}, 时间分数阈值={time_fractional_threshold:.1f}, 模数超量={modular_excess:.1f}, 周期学习失衡度={cyclical_learning_imbalance:.2f}, 学习节奏紊乱度={learning_rhythm_disruption:.1f}%"

        # 条件判断9: if w / 2 + y > z + 50 (参与度一半加掌握度超出时长加50的基准)
        if w / 2 + y > z + 50:
            type_code = 'C3'
            half_participation_mastery = w / 2 + y
            time_baseline_adjustment = z + 50
            learning_intensity_excess = half_participation_mastery - time_baseline_adjustment
            engagement_time_imbalance = learning_intensity_excess / time_baseline_adjustment if time_baseline_adjustment > 0 else float('inf')
            learning_rhythm_disruption = min(engagement_time_imbalance * 27, 95)
            analysis_detail = f"学习节奏紊乱分析: 半参与掌握度={half_participation_mastery:.1f}, 时间基线调整={time_baseline_adjustment:.1f}, 学习强度超量={learning_intensity_excess:.1f}, 参与时间失衡度={engagement_time_imbalance:.2f}, 学习节奏紊乱度={learning_rhythm_disruption:.1f}%"
        # 条件判断10: C4
        if y ** 2 / (w + 1) > z + 100:
            type_code = 'C4'
            mastery_participation_mismatch = (y ** 2 / (w + 1)) - (z + 100)
            participation_mismatch = min(mastery_participation_mismatch * 0.6, 95)
            analysis_detail = f"掌握度参与失配分析: 掌握参与比={y ** 2 / (w + 1):.2f}, 时长基准={z + 100:.1f}, 失配量={mastery_participation_mismatch:.1f}, 失配度={participation_mismatch:.1f}%"

        # 条件判断11: C5
        if (y + z) % 30 < w / 5:
            type_code = 'C5'
            cycle_sync_anomaly = (w / 5) - ((y + z) % 30)
            learning_cycle_desync = min(cycle_sync_anomaly * 4, 95)
            analysis_detail = f"学习周期同步异常分析: 掌握时长余数={(y + z) % 30:.1f}, 参与度基数={w / 5:.1f}, 同步差={cycle_sync_anomaly:.1f}, 异常度={learning_cycle_desync:.1f}%"

        # 条件判断12: C6
        if w * 3 - y > z / 2 + 20:
            type_code = 'C6'
            interaction_intensity_excess = (w * 3 - y) - (z / 2 + 20)
            intensity_overload = min(interaction_intensity_excess * 1.3, 95)
            analysis_detail = f"互动强度超载分析: 互动掌握差={w * 3 - y:.1f}, 时长基准={z / 2 + 20:.1f}, 超载量={interaction_intensity_excess:.1f}, 超载度={intensity_overload:.1f}%"

        # 条件判断13: C7
        if z / (w + 1) > y / 10 + 15:
            type_code = 'C7'
            time_participation_ratio_imbalance = (z / (w + 1)) - (y / 10 + 15)
            ratio_imbalance = min(time_participation_ratio_imbalance * 2, 95)
            analysis_detail = f"时长参与比例失调分析: 时长参与比={z / (w + 1):.2f}, 掌握度基准={y / 10 + 15:.2f}, 失调度={ratio_imbalance:.1f}%"
        # 发送分析结果回主进程
        result = {'code': type_code, 'detail': analysis_detail}
        comm.send(result, dest=0, tag=200)


    elif rank == 3:
        # 进程3：接收 z, w, m 进行平台优化分析
        z = comm.recv(source=0, tag=1, status=status)
        w = comm.recv(source=0, tag=2, status=status)
        m = comm.recv(source=0, tag=3, status=status)

        type_code = 'D0'  # 默认为平台优化平衡
        analysis_detail = ""

        # 条件判断10: if z > w + m ** 3 (时长超出参与度加平台适配度立方)
        if z > w + m ** 3:
            type_code = 'D1'
            daily_study_duration = z
            participation_platform_cubic = w + m ** 3
            time_investment_surplus = daily_study_duration - participation_platform_cubic
            learning_efficiency_deterioration = time_investment_surplus / participation_platform_cubic if participation_platform_cubic > 0 else float('inf')
            time_utilization_inefficiency = min(learning_efficiency_deterioration * 30, 95)
            analysis_detail = f"时间利用低效分析: 日学习时长={daily_study_duration}分钟, 参与平台立方和={participation_platform_cubic:.1f}, 时间投入盈余={time_investment_surplus:.1f}, 学习效率恶化度={learning_efficiency_deterioration:.2f}, 时间利用低效度={time_utilization_inefficiency:.1f}%"

        # 条件判断11: if m * w / 2 < z - 100 (平台参与度积的一半低于时长减100)
        if m * w / 2 < z - 100:
            type_code = 'D2'
            platform_participation_half_product = m * w / 2
            adjusted_time_threshold = z - 100
            platform_engagement_deficit = adjusted_time_threshold - platform_participation_half_product
            platform_utilization_gap_ratio = platform_engagement_deficit / platform_participation_half_product if platform_participation_half_product > 0 else float('inf')
            platform_engagement_underperformance = min(platform_utilization_gap_ratio * 25, 95)
            analysis_detail = f"平台参与表现不足分析: 平台参与半积={platform_participation_half_product:.1f}, 调整时间阈值={adjusted_time_threshold:.1f}, 平台参与缺口={platform_engagement_deficit:.1f}, 平台利用率差距比={platform_utilization_gap_ratio:.2f}, 平台参与表现不足度={platform_engagement_underperformance:.1f}%"

        # 条件判断12: if (z - w) / m > 30 (时长减参与度除以平台适配度超出30)
        if (z - w) / m > 30:
            type_code = 'D3'
            time_participation_gap = z - w
            platform_adaptation_factor = m
            gap_adaptation_ratio = time_participation_gap / platform_adaptation_factor if platform_adaptation_factor > 0 else float('inf')
            adaptation_threshold = 30
            platform_adaptation_stress = gap_adaptation_ratio - adaptation_threshold
            platform_optimization_failure = min(platform_adaptation_stress / adaptation_threshold * 100, 95)
            analysis_detail = f"平台优化失效分析: 时长参与缺口={time_participation_gap:.1f}, 平台适配因子={platform_adaptation_factor}, 缺口适配比={gap_adaptation_ratio:.1f}, 适配阈值={adaptation_threshold}, 平台适配压力={platform_adaptation_stress:.1f}, 平台优化失效度={platform_optimization_failure:.1f}%"

        # 条件判断13: D4
        if (z + w) / 2 > m ** 2 + 50:
            type_code = 'D4'
            platform_load_shortage = ((z + w) / 2) - (m ** 2 + 50)
            capacity_insufficiency = min(platform_load_shortage * 1.1, 95)
            analysis_detail = f"平台承载力不足分析: 时长参与均值={(z + w) / 2:.1f}, 平台容量={m ** 2 + 50:.1f}, 承载缺口={platform_load_shortage:.1f}, 不足度={capacity_insufficiency:.1f}%"

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
    learning_data, analysis_results = mpi_learning_analysis()

    # 只在主进程中进行输出
    if rank == 0 and learning_data is not None:
        x, y, z, w, m = learning_data

        print("=" * 70)
        print("  智能学习平台分析系统 - MPI并行计算版本  ")
        print("=" * 70)
        print()

        print("--- 实时学习数据 ---")
        print(f"学习进度(X): {x}%")
        print(f"知识掌握度(Y): {y}%")
        print(f"学习时长(Z): {z} 分钟/天")
        print(f"互动参与度(W): {w}%")
        print(f"平台适配度(M): {m} 分")
        print()

        print("--- 学习平台综合分析报告 ---")
        for i, result in enumerate(analysis_results, 1):
            print(f"{i}. {result}")
        print()

        print("=" * 70)
        print("MPI并行分析完成 - 4个进程同时工作")
        print("=" * 70)


if __name__ == "__main__":
    main()