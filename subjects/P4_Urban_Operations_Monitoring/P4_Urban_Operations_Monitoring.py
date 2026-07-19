from mpi4py import MPI
import random
import math

# --- 程序1：交通流量监控分析 (Ranks 0-3) ---
TRAFFIC_TYPE_DEF = {
    # 宏观交通效率分析 (A0-A3)
    'A0': '交通效率平衡',
    'A1': '车流密度过载',
    'A2': '驾驶环境失配',
    'A3': '交通协调失衡',
    'A4': '车流通畅配合和超限',
    'A5': '通畅配合平方收敛状态',
    'A6': '车流配合和异常',
    'A7': '车流配合倒数和超限',

    # 流量信号协调分析 (B0-B3)
    'B0': '流量信号平衡',
    'B1': '信号响应滞后',
    'B2': '流量信号同步异常',
    'B3': '信号控制超载',
    'B4': '车流信号积超限',
    'B5': '平均值信号失衡',
    'B6': '车流通畅和信号异常',
    # 驾驶天气适应分析 (C0-C3)
    'C0': '驾驶天气协调',
    'C1': '适应性超载',
    'C2': '协调强化异常',
    'C3': '立体适应失衡',
    'C4': '通畅配合积信号超限',
    'C5': '平方和收敛状态',

    # 交通优化分析 (D0-D3)
    'D0': '交通优化平衡',
    'D1': '三维协调异常',
    'D2': '环境适应不足',
    'D3': '周期性优化异常',
    'D4': '信号配合积天气超限',
    'D5': '平均值收敛状态',
    'D6': '配合平方天气超限',
}

# --- 程序2：环境质量监测分析 (Ranks 4-7) ---
ENVIRONMENTAL_TYPE_DEF = {
    # 宏观环境质量分析 (A0-A3)
    'A0': '环境质量平衡',
    'A1': '综合污染超标',
    'A2': '生态平衡失调',
    'A3': '气象环境失衡',
    'A4': '空气噪音绿化污染和超限',
    'A5': '综合平方收敛状态',
    'A6': '空气噪音和异常',
    # 空气噪音平衡分析 (B0-B3)
    'B0': '空气噪音平衡',
    'B1': '空气质量调节异常',
    'B2': '污染立方承载超限',
    'B3': '环境健康水平不足',
    'B4': '空气噪音和绿化超限',
    'B5': '平均值绿化失衡',
    # 污染气象关联分析 (C0-C3)
    'C0': '污染气象协调',
    'C1': '噪音污染调节失效',
    'C2': '环境周期同步异常',
    'C3': '污染净化能力超载',
    'C4': '噪音污染和绿化超限',
    'C5': '平方和收敛状态',
    'C6': '倒数和超限',
    # 环境优化分析 (D0-D3)
    'D0': '环境优化平衡',
    'D1': '气象优化潜力不足',
    'D2': '环境改善效果异常',
    'D3': '系统承载阈值超限',
    'D4': '绿化气象积污染超限',
    'D5': '平均值收敛状态',
    'D6': '污染平方气象超限',
    'D7': '倒数和超限',
}

# --- 程序3：能源消耗分析 (Ranks 8-11) ---
ENERGY_TYPE_DEF = {
    # 宏观能源效率分析 (A0-A3)
    'A0': '能源效率平衡',
    'A1': '负荷调节异常',
    'A2': '设备效率失配',
    'A3': '综合能源不协调',
    'A4': '负荷效率峰值可再生和超限',
    'A5': '综合平方收敛状态',
    'A6': '负荷效率和异常',
    # 负荷效率平衡分析 (B0-B3)
    'B0': '负荷效率平衡',
    'B1': '动态功率超载',
    'B2': '电力波动异常',
    'B3': '系统功率缺口过大',
    'B4': '负荷效率和峰值超限',
    'B5': '平均值峰值失衡',
    'B6': '负荷效率和峰值异常',
    'B7': '负荷峰值倒数超限',

    # 可再生能源协调分析 (C0-C3)
    'C0': '可再生能源协调',
    'C1': '清洁能源调节不足',
    'C2': '能源调节阈值超限',
    'C3': '完美能源匹配异常',
    'C4': '效率可再生和峰值超限',
    'C5': '平方和收敛状态',
    'C6': '倒数和超限',
    # 能源优化分析 (D0-D3)
    'D0': '能源优化平衡',
    'D1': '峰值设备功率超载',
    'D2': '系统优化阈值超限',
    'D3': '能源同步异常',
    'D4': '峰值可再生积设备超限',
    'D5': '平均值收敛状态',
}

# --- 程序4：公共安全评估分析 (Ranks 12-15) ---
SAFETY_TYPE_DEF = {
    # 宏观公共安全分析 (A0-A3)
    'A0': '公共安全平衡',
    'A1': '分式协调异常',
    'A2': '比例协调不足',
    'A3': '多项式安全超载',
    'A4': '响应警力监控安全和超限',
    'A5': '综合平方收敛状态',

    # 安全响应协调分析 (B0-B3)
    'B0': '安全响应协调',
    'B1': '嵌套响应异常',
    'B2': '乘积模运算异常',
    'B3': '响应监控平方不足',
    'B4': '响应警力积监控超限',
    'B5': '平均值监控失衡',
    'B6': '平方和监控异常',

    # 警力监控协调分析 (C0-C3)
    'C0': '警力监控协调',
    'C1': '分式警力超载',
    'C2': '警力监控比例失调',
    'C3': '完美协调匹配异常',
    'C4': '警力安全和监控超限',
    'C5': '平方和收敛状态',
    'C6': '倒数和超限',
    'C7': '平方和监控异常',

    # 安全优化分析 (D0-D3)
    'D0': '安全优化平衡',
    'D1': '连续运算超载',
    'D2': '平方除法异常',
    'D3': '多重模运算异常',
    'D4': '监控安全和设施超限',
    'D5': '平均值收敛状态',
    'D6': '安全平方设施超限',
    'D7': '倒数和超限',
}

# --- 程序5：物流配送分析 (Ranks 16-19) ---
LOGISTICS_TYPE_DEF = {
    # 宏观配送效率分析 (A0-A3)
    'A0': '配送效率平衡',
    'A1': '订单负载超限',
    'A2': '效率匹配不足',
    'A3': '综合配送失衡',
    'A4': '订单压力指数异常',
    'A5': '多维配送协调失衡',
    'A6': '动态负载波动异常',
    # 订单效率平衡分析 (B0-B3)
    'B0': '订单效率平衡',
    'B1': '平方效率异常',
    'B2': '订单波动超限',
    'B3': '效率缺口过大',
    'B4': '订单密度梯度超载',
    'B5': '效率路径乘积饱和',
    # 路径车辆协调分析 (C0-C3)
    'C0': '路径车辆协调',
    'C1': '路径优化不足',
    'C2': '车辆协调异常',
    'C3': '周期同步失调',
    'C4': '三维效率协调超载',
    'C5': '车辆效率平方根调节异常',
    'C6': '路径车辆除法协调失调',
    # 配送优化分析 (D0-D3)
    'D0': '配送优化平衡',
    'D1': '立方负载超限',
    'D2': '服务质量异常',
    'D3': '综合优化超载',
    'D4': '路径车辆乘积与服务平方对比',
    'D5': '多重除法嵌套调节异常',
    'D6': '服务驱动的路径车辆比失衡',
    'D7': '车辆路径差值平方异常',

}
# --- 程序6：人口流动监控分析 (Ranks 20-23) ---
POPULATION_TYPE_DEF = {
    # 宏观人口流动分析 (A0-A3)
    'A0': '人口流动平衡',
    'A1': '流动密度平方差异常',
    'A2': '分数幂组合不足',
    'A3': '多次幂组合超载',
    'A4': '流动密度梯度与设施幂次对比',
    'A5': '多重开方嵌套组合',
    # 流动密度平衡分析 (B0-B3)
    'B0': '流动密度平衡',
    'B1': '二次方程失衡',
    'B2': '交叉比值异常',
    'B3': '分数幂阈值超限',
    'B4': '流动速度与密度的对数级关系异常',
    'B5': '嵌套平方根与分布的复合关系',
    'B6': '分布驱动的流动密度非线性调节',
    'B7': '流动密度交互的分段幂次分析',
    # 分布多样性协调分析 (C0-C3)
    'C0': '分布多样性协调',
    'C1': '分数幂乘积不足',
    'C2': '平方比例异常',
    'C3': '分数加权和不足',
    'C4': '密度年龄几何平均与分布的幂次对比',
    'C5': '分布驱动的密度年龄多项式组合',
    'C6': '密度年龄差值的非线性转换异常',
    'C7': '多重分数幂加权协调失衡',
    # 人口优化分析 (D0-D3)
    'D0': '人口优化平衡',
    'D1': '立方和超载',
    'D2': '开方平方组合异常',
    'D3': '加权平均对比异常',
    'D4': '分布年龄乘积的对数变换与设施关系',
    'D5': '三变量调和平均与幂次组合',
    'D6': '年龄设施非线性交互与分布对比',
    'D7': '分布年龄差值的平方根比值异常',
}

# --- 程序6 (Ranks 20-23) - 待添加 ---

def main():
    """主控制函数：路由到不同的MPI程序"""
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    status = MPI.Status()

    if size != 24:
        if rank == 0:
            print(f"警告：此程序最终设计为 24 个进程，但当前启动了 {size} 个。")
            print("程序将只运行已实现的部分。")
        # (我们不会退出，以便可以测试已实现的部分)

    # --- 路由到不同的程序 ---

    # -----------------------------------------------------------------
    # --- 程序1：交通流量监控分析 (Ranks 0-3) ---
    # -----------------------------------------------------------------
    if rank == 0:
        # 进程0：主进程：负责数据生成、分发和宏观交通效率分析

        # 1. 随机生成五个核心交通监控变量
        x = random.randint(50, 2000)  # 车流密度 (辆/小时)
        y = random.randint(20, 100)  # 道路通畅度 (%)
        z = random.randint(30, 180)  # 信号灯响应时间 (秒)
        w = random.randint(40, 100)  # 驾驶员配合度 (%)
        m = random.randint(1, 10)  # 天气影响因子 (1-10分)

        # 存储数据供main函数访问
        traffic_data = [x, y, z, w, m]

        # 2. 分发数据到其他进程
        # 发给进程1：x, y, z (流量信号协调分析)
        comm.send(x, dest=1, tag=1)
        comm.send(y, dest=1, tag=2)
        comm.send(z, dest=1, tag=3)

        # 发给进程2：y, z, w (驾驶天气适应分析)
        comm.send(y, dest=2, tag=1)
        comm.send(z, dest=2, tag=2)
        comm.send(w, dest=2, tag=3)

        # 发给进程3：z, w, m (交通优化分析)
        comm.send(z, dest=3, tag=1)
        comm.send(w, dest=3, tag=2)
        comm.send(m, dest=3, tag=3)

        # 3. 执行宏观交通效率分析 (xyzwm)
        type_code = 'A0'  # 默认为交通效率平衡状态
        analysis_detail = ""

        # 条件判断1: if x > y * z - 500
        if x > y * z - 500:
            type_code = 'A1'
            vehicle_flow_density = x
            smoothness_signal_capacity = y * z - 500
            density_overflow = vehicle_flow_density - smoothness_signal_capacity
            traffic_saturation_ratio = vehicle_flow_density / smoothness_signal_capacity if smoothness_signal_capacity > 0 else float(
                'inf')
            congestion_pressure_level = min(traffic_saturation_ratio * 35, 100)
            analysis_detail = f"车流过载分析: 车流密度={vehicle_flow_density}辆/h, 通畅信号容量={smoothness_signal_capacity:.1f}, 密度溢出={density_overflow:.1f}辆/h, 交通饱和比={traffic_saturation_ratio:.2f}, 拥堵压力水平={congestion_pressure_level:.1f}%"

        # 条件判断2: if w ** 2 < m * 100
        if w ** 2 < m * 100:
            type_code = 'A2'
            driver_cooperation_squared = w ** 2
            weather_impact_baseline = m * 100
            cooperation_deficit = weather_impact_baseline - driver_cooperation_squared
            environmental_mismatch_factor = cooperation_deficit / driver_cooperation_squared if driver_cooperation_squared > 0 else float(
                'inf')
            driving_environment_stress = min(environmental_mismatch_factor * 28, 95)
            analysis_detail = f"驾驶环境失配分析: 配合度平方={driver_cooperation_squared}, 天气影响基线={weather_impact_baseline:.1f}, 配合缺口={cooperation_deficit:.1f}, 环境失配因子={environmental_mismatch_factor:.2f}, 驾驶环境压力={driving_environment_stress:.1f}%"

        # 条件判断3: if x + w > y + z * 2
        if x + w > y + z * 2:
            type_code = 'A3'
            traffic_cooperation_aggregate = x + w
            road_signal_coordination = y + z * 2
            coordination_imbalance = traffic_cooperation_aggregate - road_signal_coordination
            system_coordination_strain = coordination_imbalance / road_signal_coordination if road_signal_coordination > 0 else float(
                'inf')
            comprehensive_traffic_stress = min(system_coordination_strain * 24, 95)
            analysis_detail = f"交通协调失衡分析: 交通配合聚合={traffic_cooperation_aggregate:.1f}, 道路信号协调={road_signal_coordination:.1f}, 协调失衡量={coordination_imbalance:.1f}, 系统协调张力={system_coordination_strain:.2f}, 综合交通压力={comprehensive_traffic_stress:.1f}%"
        # 条件判断4: A4
        if x / 10 > y + z + w:
            type_code = 'A4'
            traffic_flow_scaled = x / 10
            smoothness_signal_cooperation_sum = y + z + w
            analysis_detail = f"车流通畅配合和超限分析: 车流缩放={traffic_flow_scaled:.2f}辆/h, 通畅信号配合和={smoothness_signal_cooperation_sum:.1f}, 和超限度={min((traffic_flow_scaled - smoothness_signal_cooperation_sum) * 0.5, 95):.1f}%"

        # 条件判断5: A5
        if (y + w) ** 2 / 100 < z + m * 20:
            type_code = 'A5'
            smoothness_cooperation_square_scaled = (y + w) ** 2 / 100
            signal_weather_sum = z + m * 20
            analysis_detail = f"通畅配合平方收敛状态分析: 通畅配合平方缩放={(y + w) ** 2 / 100:.2f}, 信号天气和={signal_weather_sum:.1f}, 收敛优化度={min((signal_weather_sum - smoothness_cooperation_square_scaled) * 0.3, 95):.1f}%"

        # 条件判断6: A6
        if x / 100 + w > y * m + z:
            type_code = 'A6'
            flow_cooperation_sum = x / 100 + w
            smoothness_weather_signal_threshold = y * m + z
            analysis_detail = f"车流配合和异常分析: 车流配合和={flow_cooperation_sum:.2f}, 通畅天气信号阈值={smoothness_weather_signal_threshold:.1f}, 和异常度={min((flow_cooperation_sum - smoothness_weather_signal_threshold) * 0.8, 95):.1f}%"

        # 条件判断7: A7
        if x / (y + 1) + w / (m + 1) > z * 2:
            type_code = 'A7'
            flow_cooperation_reciprocal_sum = x / (y + 1) + w / (m + 1)
            signal_threshold = z * 2
            analysis_detail = f"车流配合倒数和超限分析: 车流配合倒数和={flow_cooperation_reciprocal_sum:.2f}, 信号阈值={signal_threshold:.1f}, 倒数和超限度={min((flow_cooperation_reciprocal_sum - signal_threshold) * 0.6, 95):.1f}%"

        # 4. 收集其他进程的分析结果
        flow_signal_result = comm.recv(source=1, tag=100, status=status)
        driving_weather_result = comm.recv(source=2, tag=200, status=status)
        traffic_optimization_result = comm.recv(source=3, tag=300, status=status)

        # 5. 组装完整结果
        analysis_results = [
            f"宏观交通效率 (xyzwm): {type_code} -> {TRAFFIC_TYPE_DEF.get(type_code, '未知')} | {analysis_detail}",
            f"流量信号协调 (xyz): {flow_signal_result['code']} -> {TRAFFIC_TYPE_DEF.get(flow_signal_result['code'], '未知')} | {flow_signal_result['detail']}",
            f"驾驶天气适应 (yzw): {driving_weather_result['code']} -> {TRAFFIC_TYPE_DEF.get(driving_weather_result['code'], '未知')} | {driving_weather_result['detail']}",
            f"交通优化分析 (zwm): {traffic_optimization_result['code']} -> {TRAFFIC_TYPE_DEF.get(traffic_optimization_result['code'], '未知')} | {traffic_optimization_result['detail']}"
        ]

        # 6. 打印报告
        print("=" * 70)
        print(f"  交通流量监控系统 (进程 0-3)  ")
        print("=" * 70)
        print()
        print("--- 实时交通监控数据 ---")
        print(f"车流密度(X): {x} 辆/小时")
        print(f"道路通畅度(Y): {y}%")
        print(f"信号灯响应时间(Z): {z} 秒")
        print(f"驾驶员配合度(W): {w}%")
        print(f"天气影响因子(M): {m} 分")
        print()
        print("--- 交通流量综合分析报告 ---")
        for i, result in enumerate(analysis_results, 1):
            print(f"{i}. {result}")
        print()
        print("=" * 70)
        print(f"程序1 (Ranks 0-3) 分析完成")
        print("=" * 70)
        print("\n")  # 增加间距


    elif rank == 1:
        # 进程1：接收 x, y, z 进行流量信号协调分析
        x = comm.recv(source=0, tag=1, status=status)
        y = comm.recv(source=0, tag=2, status=status)
        z = comm.recv(source=0, tag=3, status=status)

        type_code = 'B0'  # 默认为流量信号平衡
        analysis_detail = ""

        # 条件判断4: if z ** 2 > x + y ** 2
        if z ** 2 > x + y ** 2:
            type_code = 'B1'
            signal_response_squared = z ** 2
            traffic_smoothness_quadratic = x + y ** 2
            quadratic_response_excess = signal_response_squared - traffic_smoothness_quadratic
            signal_lag_amplification = quadratic_response_excess / traffic_smoothness_quadratic if traffic_smoothness_quadratic > 0 else float(
                'inf')
            signal_response_delay_level = min(signal_lag_amplification * 32, 95)
            analysis_detail = f"信号响应滞后分析: 信号响应平方={signal_response_squared}, 交通通畅二次={traffic_smoothness_quadratic:.1f}, 二次响应超量={quadratic_response_excess:.1f}, 信号滞后放大度={signal_lag_amplification:.2f}, 信号响应延迟水平={signal_response_delay_level:.1f}%"

        # 条件判断5: if x % y == z % 15
        if x % y == z % 15:
            type_code = 'B2'
            traffic_flow_modulus = x % y if y > 0 else 0
            signal_time_modulus = z % 15
            modular_synchronization_value = traffic_flow_modulus
            perfect_sync_indicator = 1 if traffic_flow_modulus == signal_time_modulus else 0
            synchronization_anomaly_score = perfect_sync_indicator * 90 + (
                        15 - abs(traffic_flow_modulus - signal_time_modulus)) * 5
            analysis_detail = f"流量信号同步异常分析: 交通流模数={traffic_flow_modulus}, 信号时间模数={signal_time_modulus}, 模运算同步值={modular_synchronization_value}, 完美同步指示={perfect_sync_indicator}, 同步异常评分={synchronization_anomaly_score:.1f}%"

        # 条件判断6: if x * y > z ** 3 - 2000
        if x * y > z ** 3 - 2000:
            type_code = 'B3'
            traffic_flow_smoothness_product = x * y
            signal_cubic_capacity = z ** 3 - 2000
            flow_control_overload = traffic_flow_smoothness_product - signal_cubic_capacity
            cubic_control_strain = flow_control_overload / signal_cubic_capacity if signal_cubic_capacity > 0 else float(
                'inf')
            signal_control_saturation = min(cubic_control_strain * 18, 95)
            analysis_detail = f"信号控制超载分析: 交通流通畅乘积={traffic_flow_smoothness_product}, 信号立方容量={signal_cubic_capacity:.1f}, 流控过载量={flow_control_overload:.1f}, 立方控制张力={cubic_control_strain:.2f}, 信号控制饱和度={signal_control_saturation:.1f}%"
        # 条件判断7: B4
        if x / 10 > y * z + 100:
            type_code = 'B4'
            flow_density_scaled = x / 10
            smoothness_signal_product_threshold = y * z + 100
            analysis_detail = f"车流信号积超限分析: 车流密度缩放={flow_density_scaled:.2f}辆/h, 通畅信号积阈值={smoothness_signal_product_threshold:.1f}, 积超限度={min((flow_density_scaled - smoothness_signal_product_threshold) * 0.2, 95):.1f}%"

        # 条件判断8: B5
        if (x / 100 + y) / 2 > z + 50:
            type_code = 'B5'
            flow_smoothness_average = (x / 100 + y) / 2
            signal_threshold = z + 50
            analysis_detail = f"平均值信号失衡分析: 车流通畅均值={(x / 100 + y) / 2:.2f}, 信号阈值={signal_threshold:.1f}, 平均失衡度={min((flow_smoothness_average - signal_threshold) * 0.8, 95):.1f}%"

        # 条件判断9: B6
        if x / 100 + y > z * 2 + 80:
            type_code = 'B6'
            flow_smoothness_sum = x / 100 + y
            signal_multiple_threshold = z * 2 + 80
            analysis_detail = f"车流通畅和信号异常分析: 车流通畅和={flow_smoothness_sum:.2f}, 信号倍数阈值={signal_multiple_threshold:.1f}, 和异常度={min((flow_smoothness_sum - signal_multiple_threshold) * 0.4, 95):.1f}%"

        # 发送分析结果回主进程
        result = {'code': type_code, 'detail': analysis_detail}
        comm.send(result, dest=0, tag=100)


    elif rank == 2:
        # 进程2：接收 y, z, w 进行驾驶天气适应分析
        y = comm.recv(source=0, tag=1, status=status)
        z = comm.recv(source=0, tag=2, status=status)
        w = comm.recv(source=0, tag=3, status=status)

        type_code = 'C0'  # 默认为驾驶天气协调
        analysis_detail = ""

        # 条件判断7: if w + y > z ** 2 / 4
        if w + y > z ** 2 / 4:
            type_code = 'C1'
            cooperation_smoothness_sum = w + y
            signal_quadratic_threshold = z ** 2 / 4
            adaptability_overflow = cooperation_smoothness_sum - signal_quadratic_threshold
            adaptation_intensity_ratio = cooperation_smoothness_sum / signal_quadratic_threshold if signal_quadratic_threshold > 0 else float(
                'inf')
            adaptability_overload_stress = min(adaptation_intensity_ratio * 29, 95)
            analysis_detail = f"适应性超载分析: 配合通畅和={cooperation_smoothness_sum:.1f}, 信号二次阈值={signal_quadratic_threshold:.1f}, 适应性溢出={adaptability_overflow:.1f}, 适应强度比={adaptation_intensity_ratio:.2f}, 适应性过载压力={adaptability_overload_stress:.1f}%"

        # 条件判断8: if (y * w) ** 2 > z * 800
        if (y * w) ** 2 > z * 800:
            type_code = 'C2'
            smoothness_cooperation_squared = (y * w) ** 2
            signal_amplified_threshold = z * 800
            quadratic_coordination_excess = smoothness_cooperation_squared - signal_amplified_threshold
            coordination_amplification_factor = smoothness_cooperation_squared / signal_amplified_threshold if signal_amplified_threshold > 0 else float(
                'inf')
            coordination_enhancement_anomaly = min(coordination_amplification_factor * 22, 95)
            analysis_detail = f"协调强化异常分析: 通畅配合平方={smoothness_cooperation_squared:.1f}, 信号放大阈值={signal_amplified_threshold:.1f}, 二次协调超量={quadratic_coordination_excess:.1f}, 协调放大因子={coordination_amplification_factor:.2f}, 协调强化异常度={coordination_enhancement_anomaly:.1f}%"

        # 条件判断9: if y ** 3 - w ** 3 > z * 30
        if y ** 3 - w ** 3 > z * 30:
            type_code = 'C3'
            smoothness_cubed = y ** 3
            cooperation_cubed = w ** 3
            cubic_difference = smoothness_cubed - cooperation_cubed
            signal_cubic_benchmark = z * 30
            cubic_imbalance_excess = cubic_difference - signal_cubic_benchmark
            spatial_adaptation_distortion = cubic_imbalance_excess / signal_cubic_benchmark if signal_cubic_benchmark > 0 else float(
                'inf')
            three_dimensional_adaptation_stress = min(spatial_adaptation_distortion * 26, 95)
            analysis_detail = f"立体适应失衡分析: 通畅度立方={smoothness_cubed}, 配合度立方={cooperation_cubed}, 立方差值={cubic_difference:.1f}, 信号立方基准={signal_cubic_benchmark:.1f}, 立方失衡超量={cubic_imbalance_excess:.1f}, 三维适应压力={three_dimensional_adaptation_stress:.1f}%"
        # 条件判断10: C4
        if y * w / 100 > z + 50:
            type_code = 'C4'
            smoothness_cooperation_product_scaled = y * w / 100
            signal_threshold = z + 50
            analysis_detail = f"通畅配合积信号超限分析: 通畅配合积缩放={smoothness_cooperation_product_scaled:.2f}, 信号阈值={signal_threshold:.1f}, 积超限度={min((smoothness_cooperation_product_scaled - signal_threshold) * 0.5, 95):.1f}%"

        # 条件判断11: C5
        if (y + w) ** 2 / 100 < z ** 2 + 100:
            type_code = 'C5'
            smoothness_cooperation_square_scaled = (y + w) ** 2 / 100
            signal_squared_threshold = z ** 2 + 100
            analysis_detail = f"平方和收敛状态分析: 通畅配合平方缩放={(y + w) ** 2 / 100:.2f}, 信号平方阈值={signal_squared_threshold:.1f}, 收敛优化度={min((signal_squared_threshold - smoothness_cooperation_square_scaled) * 0.02, 95):.1f}%"

        # 发送分析结果回主进程
        result = {'code': type_code, 'detail': analysis_detail}
        comm.send(result, dest=0, tag=200)


    elif rank == 3:
        # 进程3：接收 z, w, m 进行交通优化分析
        z = comm.recv(source=0, tag=1, status=status)
        w = comm.recv(source=0, tag=2, status=status)
        m = comm.recv(source=0, tag=3, status=status)

        type_code = 'D0'  # 默认为交通优化平衡
        analysis_detail = ""

        # 条件判断10: if z * w * m > 8000
        if z * w * m > 8000:
            type_code = 'D1'
            three_dimensional_coordination = z * w * m
            optimization_threshold = 8000
            spatial_coordination_overflow = three_dimensional_coordination - optimization_threshold
            three_factor_interaction_intensity = three_dimensional_coordination / optimization_threshold
            multi_dimensional_coordination_anomaly = min(three_factor_interaction_intensity * 25, 95)
            analysis_detail = f"三维协调异常分析: 三维协调值={three_dimensional_coordination}, 优化阈值={optimization_threshold}, 空间协调溢出={spatial_coordination_overflow:.1f}, 三因子交互强度={three_factor_interaction_intensity:.2f}, 多维协调异常度={multi_dimensional_coordination_anomaly:.1f}%"

        # 条件判断11: if (z + w) ** 2 < m * 400
        if (z + w) ** 2 < m * 400:
            type_code = 'D2'
            signal_cooperation_squared = (z + w) ** 2
            weather_adaptation_capacity = m * 400
            quadratic_adaptation_deficit = weather_adaptation_capacity - signal_cooperation_squared
            environmental_adaptation_insufficiency = quadratic_adaptation_deficit / signal_cooperation_squared if signal_cooperation_squared > 0 else float(
                'inf')
            weather_adaptation_underperformance = min(environmental_adaptation_insufficiency * 33, 95)
            analysis_detail = f"环境适应不足分析: 信号配合平方={signal_cooperation_squared:.1f}, 天气适应容量={weather_adaptation_capacity:.1f}, 二次适应缺口={quadratic_adaptation_deficit:.1f}, 环境适应不足度={environmental_adaptation_insufficiency:.2f}, 天气适应表现不足={weather_adaptation_underperformance:.1f}%"

        # 条件判断12: if z % (w + 1) > m ** 2
        if z % (w + 1) > m ** 2:
            type_code = 'D3'
            signal_modular_remainder = z % (w + 1) if (w + 1) > 0 else 0
            weather_squared_threshold = m ** 2
            modular_excess = signal_modular_remainder - weather_squared_threshold
            cyclical_optimization_imbalance = modular_excess / weather_squared_threshold if weather_squared_threshold > 0 else float(
                'inf')
            periodic_optimization_distortion = min(cyclical_optimization_imbalance * 40, 95)
            analysis_detail = f"周期性优化异常分析: 信号模运算余数={signal_modular_remainder}, 天气平方阈值={weather_squared_threshold}, 模数超量={modular_excess:.1f}, 周期优化失衡度={cyclical_optimization_imbalance:.2f}, 周期性优化扭曲度={periodic_optimization_distortion:.1f}%"
        # 条件判断13: D4
        if z * w / 100 > m ** 2 + 50:
            type_code = 'D4'
            signal_cooperation_product_scaled = z * w / 100
            weather_squared_threshold = m ** 2 + 50
            analysis_detail = f"信号配合积天气超限分析: 信号配合积缩放={signal_cooperation_product_scaled:.2f}, 天气平方阈值={weather_squared_threshold:.1f}, 积超限度={min((signal_cooperation_product_scaled - weather_squared_threshold) * 0.4, 95):.1f}%"

        # 条件判断14: D5
        if (z + w) / 2 < m * 20 + 80:
            type_code = 'D5'
            signal_cooperation_average = (z + w) / 2
            weather_multiple_threshold = m * 20 + 80
            analysis_detail = f"平均值收敛状态分析: 信号配合均值={(z + w) / 2:.2f}, 天气倍数阈值={weather_multiple_threshold:.1f}, 收敛优化度={min((weather_multiple_threshold - signal_cooperation_average) * 0.5, 95):.1f}%"

        # 条件判断15: D6
        if w ** 2 / 100 > z + m * 10:
            type_code = 'D6'
            cooperation_squared_scaled = w ** 2 / 100
            signal_weather_product_threshold = z + m * 10
            analysis_detail = f"配合平方天气超限分析: 配合平方缩放={cooperation_squared_scaled:.2f}, 信号天气积阈值={signal_weather_product_threshold:.1f}, 平方超限度={min((cooperation_squared_scaled - signal_weather_product_threshold) * 0.6, 95):.1f}%"

        # 发送分析结果回主进程
        result = {'code': type_code, 'detail': analysis_detail}
        comm.send(result, dest=0, tag=300)

    # -----------------------------------------------------------------
    # --- 程序2：环境质量监测分析 (Ranks 4-7) ---
    # -----------------------------------------------------------------
    elif rank == 4:
        # 进程4：主进程 (Global Rank 4)：负责数据生成、分发和宏观环境质量分析

        # 1. 随机生成五个核心环境监测变量
        x = random.randint(0, 500)  # 空气质量指数 AQI (0-500)
        y = random.randint(40, 120)  # 噪音水平 (40-120 分贝)
        z = random.randint(10, 80)  # 绿化覆盖率 (10-80%)
        w = random.randint(5, 100)  # 污染源密度 (5-100 个/平方公里)
        m = random.randint(1, 10)  # 气象条件评分 (1-10分)

        # 存储数据供main函数访问
        environmental_data = [x, y, z, w, m]

        # 2. 分发数据到其他进程 (Ranks 5, 6, 7)
        # 发给进程 5：x, y, z (空气噪音平衡分析)
        comm.send(x, dest=5, tag=1)
        comm.send(y, dest=5, tag=2)
        comm.send(z, dest=5, tag=3)

        # 发给进程 6：y, z, w (污染气象关联分析)
        comm.send(y, dest=6, tag=1)
        comm.send(z, dest=6, tag=2)
        comm.send(w, dest=6, tag=3)

        # 发给进程 7：z, w, m (环境优化分析)
        comm.send(z, dest=7, tag=1)
        comm.send(w, dest=7, tag=2)
        comm.send(m, dest=7, tag=3)

        # 3. 执行宏观环境质量分析 (xyzwm)
        type_code = 'A0'  # 默认为环境质量平衡状态
        analysis_detail = ""

        # 条件判断1: if x ** 2 + y ** 2 > 40000
        if x ** 2 + y ** 2 > 40000:
            type_code = 'A1'
            air_quality_squared = x ** 2
            noise_level_squared = y ** 2
            comprehensive_pollution_intensity = air_quality_squared + noise_level_squared
            pollution_threshold = 40000
            pollution_intensity_excess = comprehensive_pollution_intensity - pollution_threshold
            environmental_stress_amplification = comprehensive_pollution_intensity / pollution_threshold
            comprehensive_pollution_severity = min(environmental_stress_amplification * 30, 100)
            analysis_detail = f"综合污染超标分析: 空气质量平方={air_quality_squared}, 噪音水平平方={noise_level_squared}, 综合污染强度={comprehensive_pollution_intensity:.1f}, 污染阈值={pollution_threshold}, 污染强度超量={pollution_intensity_excess:.1f}, 环境压力放大度={environmental_stress_amplification:.2f}, 综合污染严重度={comprehensive_pollution_severity:.1f}%"

        # 条件判断2: if z ** 2 + w * 15 < 800
        if z ** 2 + w * 15 < 800:
            type_code = 'A2'
            green_coverage = z
            pollution_source_density = w
            green_squared_factor = z ** 2
            pollution_linear_factor = w * 15
            ecological_balance_composite = green_squared_factor + pollution_linear_factor
            ecological_complex_threshold = 800
            ecological_composite_deficit = ecological_complex_threshold - ecological_balance_composite
            ecological_imbalance_ratio = ecological_composite_deficit / ecological_balance_composite if ecological_balance_composite > 0 else float(
                'inf')
            ecological_system_instability = min(ecological_imbalance_ratio * 38, 95)
            analysis_detail = f"生态平衡失调分析: 绿化覆盖={green_coverage}%, 污染源密度={pollution_source_density}个/平方公里, 绿化平方因子={green_squared_factor:.1f}, 污染线性因子={pollution_linear_factor:.1f}, 生态平衡复合值={ecological_balance_composite:.1f}, 生态复合阈值={ecological_complex_threshold}, 生态复合缺口={ecological_composite_deficit:.1f}, 生态失衡比={ecological_imbalance_ratio:.2f}, 生态系统不稳定度={ecological_system_instability:.1f}%"

        # 条件判断3: if m * x > y * z + 3000
        if m * x > y * z + 3000:
            type_code = 'A3'
            meteorological_air_impact = m * x
            noise_green_coordination = y * z + 3000
            meteorological_environmental_imbalance = meteorological_air_impact - noise_green_coordination
            weather_environment_dominance = meteorological_air_impact / noise_green_coordination if noise_green_coordination > 0 else float(
                'inf')
            meteorological_environmental_stress = min(weather_environment_dominance * 25, 95)
            analysis_detail = f"气象环境失衡分析: 气象空气影响={meteorological_air_impact}, 噪音绿化协调={noise_green_coordination:.1f}, 气象环境失衡量={meteorological_environmental_imbalance:.1f}, 天气环境主导度={weather_environment_dominance:.2f}, 气象环境压力={meteorological_environmental_stress:.1f}%"
        # 条件判断4: A4
        if x + y > z * 10 + w + m * 30:
            type_code = 'A4'
            air_noise_sum = x + y
            green_pollution_weather_threshold = z * 10 + w + m * 30
            analysis_detail = f"空气噪音绿化污染和超限分析: 空气噪音和={air_noise_sum:.1f}, 绿化污染天气阈值={green_pollution_weather_threshold:.1f}, 和超限度={min((air_noise_sum - green_pollution_weather_threshold) * 0.2, 95):.1f}%"

        # 条件判断5: A5
        if (x + y) ** 2 / 100 < z + w + m * 50:
            type_code = 'A5'
            air_noise_square_scaled = (x + y) ** 2 / 100
            green_pollution_weather_sum = z + w + m * 50
            analysis_detail = f"综合平方收敛状态分析: 空气噪音平方缩放={(x + y) ** 2 / 100:.2f}, 绿化污染天气和={green_pollution_weather_sum:.1f}, 收敛优化度={min((green_pollution_weather_sum - air_noise_square_scaled) * 0.15, 95):.1f}%"

        # 条件判断6: A6
        if x / 10 + y > z * m + w * 2:
            type_code = 'A6'
            air_noise_sum = x / 10 + y
            green_weather_pollution_threshold = z * m + w * 2
            analysis_detail = f"空气噪音和异常分析: 空气噪音和={air_noise_sum:.2f}, 绿化天气污染阈值={green_weather_pollution_threshold:.1f}, 和异常度={min((air_noise_sum - green_weather_pollution_threshold) * 0.5, 95):.1f}%"

        # 4. 收集其他进程的分析结果 (Ranks 5, 6, 7)
        air_noise_result = comm.recv(source=5, tag=100, status=status)
        pollution_weather_result = comm.recv(source=6, tag=200, status=status)
        environmental_optimization_result = comm.recv(source=7, tag=300, status=status)

        # 5. 组装完整结果
        analysis_results = [
            f"宏观环境质量 (xyzwm): {type_code} -> {ENVIRONMENTAL_TYPE_DEF.get(type_code, '未知')} | {analysis_detail}",
            f"空气噪音平衡 (xyz): {air_noise_result['code']} -> {ENVIRONMENTAL_TYPE_DEF.get(air_noise_result['code'], '未知')} | {air_noise_result['detail']}",
            f"污染气象关联 (yzw): {pollution_weather_result['code']} -> {ENVIRONMENTAL_TYPE_DEF.get(pollution_weather_result['code'], '未知')} | {pollution_weather_result['detail']}",
            f"环境优化分析 (zwm): {environmental_optimization_result['code']} -> {ENVIRONMENTAL_TYPE_DEF.get(environmental_optimization_result['code'], '未知')} | {environmental_optimization_result['detail']}"
        ]

        # 6. 打印报告
        print("=" * 70)
        print(f"  环境质量监测系统 (进程 4-7)  ")
        print("=" * 70)
        print()
        print("--- 实时环境监测数据 ---")
        print(f"空气质量指数(X): {x} AQI")
        print(f"噪音水平(Y): {y} 分贝")
        print(f"绿化覆盖率(Z): {z}%")
        print(f"污染源密度(W): {w} 个/平方公里")
        print(f"气象条件评分(M): {m} 分")
        print()
        print("--- 环境质量综合分析报告 ---")
        for i, result in enumerate(analysis_results, 1):
            print(f"{i}. {result}")
        print()
        print("=" * 70)
        print(f"程序2 (Ranks 4-7) 分析完成")
        print("=" * 70)
        print("\n")  # 增加间距

    elif rank == 5:
        # 进程5 (原 进程1)：接收 x, y, z 进行空气噪音平衡分析
        x = comm.recv(source=4, tag=1, status=status)
        y = comm.recv(source=4, tag=2, status=status)
        z = comm.recv(source=4, tag=3, status=status)

        type_code = 'B0'  # 默认为空气噪音平衡
        analysis_detail = ""

        # 条件判断4: if x / (y + 10) > z + 20
        if x / (y + 10) > z + 20:
            type_code = 'B1'
            air_quality_index = x
            noise_adjusted_baseline = y + 10
            air_noise_regulation_ratio = air_quality_index / noise_adjusted_baseline
            green_environment_compensation_threshold = z + 20
            regulation_threshold_excess = air_noise_regulation_ratio - green_environment_compensation_threshold
            air_quality_regulation_anomaly = regulation_threshold_excess / green_environment_compensation_threshold if green_environment_compensation_threshold > 0 else float(
                'inf')
            air_regulation_dysfunction_level = min(air_quality_regulation_anomaly * 35, 95)
            analysis_detail = f"空气质量调节异常分析: 空气质量指数={air_quality_index}, 噪音调整基线={noise_adjusted_baseline:.1f}, 空气噪音调节比={air_noise_regulation_ratio:.2f}, 绿化环境补偿阈值={green_environment_compensation_threshold:.1f}, 调节阈值超量={regulation_threshold_excess:.2f}, 空气调节功能障碍水平={air_regulation_dysfunction_level:.1f}%"

        # 条件判断5: if (x + y) ** 3 > z ** 2 * 8000
        if (x + y) ** 3 > z ** 2 * 8000:
            type_code = 'B2'
            air_noise_pollution_sum = x + y
            pollution_cubic_intensity = (x + y) ** 3
            green_squared_capacity = z ** 2 * 8000
            cubic_capacity_overflow = pollution_cubic_intensity - green_squared_capacity
            cubic_pollution_amplification = pollution_cubic_intensity / green_squared_capacity if green_squared_capacity > 0 else float(
                'inf')
            pollution_cubic_saturation = min(cubic_pollution_amplification * 20, 95)
            analysis_detail = f"污染立方承载超限分析: 空气噪音污染和={air_noise_pollution_sum}, 污染立方强度={pollution_cubic_intensity:.1f}, 绿化平方容量={green_squared_capacity:.1f}, 立方容量溢出={cubic_capacity_overflow:.1f}, 立方污染放大度={cubic_pollution_amplification:.2f}, 污染立方饱和度={pollution_cubic_saturation:.1f}%"

        # 条件判断6: if x - y + z < 120
        if x - y + z < 120:
            type_code = 'B3'
            air_quality_level = x
            noise_level = y
            green_coverage = z
            environmental_health_composite = air_quality_level - noise_level + green_coverage
            health_baseline = 120
            health_deficit = health_baseline - environmental_health_composite
            environmental_health_insufficiency = health_deficit / health_baseline
            comprehensive_health_risk = min(environmental_health_insufficiency * 45, 95)
            analysis_detail = f"环境健康水平不足分析: 空气质量水平={air_quality_level}, 噪音水平={noise_level}分贝, 绿化覆盖={green_coverage}%, 环境健康综合值={environmental_health_composite:.1f}, 健康基线={health_baseline}, 健康缺口={health_deficit:.1f}, 环境健康不足度={environmental_health_insufficiency:.2f}, 综合健康风险={comprehensive_health_risk:.1f}%"
        # 条件判断7: B4
        if x + y > z ** 2 + 200:
            type_code = 'B4'
            air_noise_sum = x + y
            green_squared_threshold = z ** 2 + 200
            analysis_detail = f"空气噪音和绿化超限分析: 空气噪音和={air_noise_sum:.1f}, 绿化平方阈值={green_squared_threshold:.1f}, 和超限度={min((air_noise_sum - green_squared_threshold) * 0.15, 95):.1f}%"

        # 条件判断8: B5
        if (x + y) / 2 > z * 8 + 100:
            type_code = 'B5'
            air_noise_average = (x + y) / 2
            green_multiple_threshold = z * 8 + 100
            analysis_detail = f"平均值绿化失衡分析: 空气噪音均值={(x + y) / 2:.2f}, 绿化倍数阈值={green_multiple_threshold:.1f}, 平均失衡度={min((air_noise_average - green_multiple_threshold) * 0.4, 95):.1f}%"

        # 发送分析结果回主进程 (Global Rank 4)
        result = {'code': type_code, 'detail': analysis_detail}
        comm.send(result, dest=4, tag=100)


    elif rank == 6:
        # 进程6 (原 进程2)：接收 y, z, w 进行污染气象关联分析
        y = comm.recv(source=4, tag=1, status=status)
        z = comm.recv(source=4, tag=2, status=status)
        w = comm.recv(source=4, tag=3, status=status)

        type_code = 'C0'  # 默认为污染气象协调
        analysis_detail = ""

        # 条件判断7: if y ** 2 / w > z * 18
        if y ** 2 / w > z * 18:
            type_code = 'C1'
            noise_squared_intensity = y ** 2
            pollution_source_density = w
            noise_pollution_intensity_ratio = noise_squared_intensity / pollution_source_density if pollution_source_density > 0 else 0
            green_regulation_capacity_multiple = z * 18
            regulation_capacity_overload = noise_pollution_intensity_ratio - green_regulation_capacity_multiple
            noise_pollution_regulation_failure = regulation_capacity_overload / green_regulation_capacity_multiple if green_regulation_capacity_multiple > 0 else float(
                'inf')
            noise_pollution_control_breakdown = min(noise_pollution_regulation_failure * 28, 95)
            analysis_detail = f"噪音污染调节失效分析: 噪音平方强度={noise_squared_intensity}, 污染源密度={pollution_source_density}个/平方公里, 噪音污染强度比={noise_pollution_intensity_ratio:.2f}, 绿化调节能力倍数={green_regulation_capacity_multiple:.1f}, 调节能力过载量={regulation_capacity_overload:.2f}, 噪音污染调节失效度={noise_pollution_regulation_failure:.2f}, 噪音污染控制崩溃度={noise_pollution_control_breakdown:.1f}%"

        # 条件判断8: if w % (y // 8) == z % 6
        if w % (y // 8) == z % 6:
            type_code = 'C2'
            pollution_source_count = w
            noise_tier = y // 8 if y >= 8 else 1
            pollution_modular_remainder = w % noise_tier if noise_tier > 0 else 0
            green_coverage = z
            green_modular_remainder = z % 6
            modular_synchronization_indicator = 1 if pollution_modular_remainder == green_modular_remainder else 0
            environmental_cyclical_synchronization_anomaly = modular_synchronization_indicator * 85 + abs(
                pollution_modular_remainder - green_modular_remainder) * 3
            analysis_detail = f"环境周期同步异常分析: 污染源数量={pollution_source_count}个/平方公里, 噪音档位={noise_tier}, 污染模数余数={pollution_modular_remainder}, 绿化覆盖={green_coverage}%, 绿化模数余数={green_modular_remainder}, 模运算同步指示={modular_synchronization_indicator}, 环境周期同步异常度={environmental_cyclical_synchronization_anomaly:.1f}%"

        # 条件判断9: if y * w ** 2 > z ** 3 + 12000
        if y * w ** 2 > z ** 3 + 12000:
            type_code = 'C3'
            noise_level = y
            pollution_density_squared = w ** 2
            noise_pollution_compound = noise_level * pollution_density_squared
            green_cubic_purification_capacity = z ** 3 + 12000
            purification_capacity_overload = noise_pollution_compound - green_cubic_purification_capacity
            pollution_purification_imbalance = purification_capacity_overload / green_cubic_purification_capacity if green_cubic_purification_capacity > 0 else float(
                'inf')
            pollution_purification_system_saturation = min(pollution_purification_imbalance * 22, 95)
            analysis_detail = f"污染净化能力超载分析: 噪音水平={noise_level}分贝, 污染密度平方={pollution_density_squared:.1f}, 噪音污染复合值={noise_pollution_compound:.1f}, 绿化立方净化容量={green_cubic_purification_capacity:.1f}, 净化容量过载量={purification_capacity_overload:.1f}, 污染净化失衡度={pollution_purification_imbalance:.2f}, 污染净化系统饱和度={pollution_purification_system_saturation:.1f}%"
        # 条件判断10: C4
        if y + w > z ** 2 + 100:
            type_code = 'C4'
            noise_pollution_sum = y + w
            green_squared_threshold = z ** 2 + 100
            analysis_detail = f"噪音污染和绿化超限分析: 噪音污染和={noise_pollution_sum:.1f}, 绿化平方阈值={green_squared_threshold:.1f}, 和超限度={min((noise_pollution_sum - green_squared_threshold) * 0.2, 95):.1f}%"

        # 条件判断11: C5
        if (y + w) ** 2 / 100 < z * 5 + 50:
            type_code = 'C5'
            noise_pollution_square_scaled = (y + w) ** 2 / 100
            green_multiple_threshold = z * 5 + 50
            analysis_detail = f"平方和收敛状态分析: 噪音污染平方缩放={(y + w) ** 2 / 100:.2f}, 绿化倍数阈值={green_multiple_threshold:.1f}, 收敛优化度={min((green_multiple_threshold - noise_pollution_square_scaled) * 0.3, 95):.1f}%"

        # 条件判断12: C6
        if y / (z + 1) + w > 80:
            type_code = 'C6'
            noise_green_pollution_sum = y / (z + 1) + w
            reciprocal_threshold = 80
            analysis_detail = f"倒数和超限分析: 噪音绿化污染和={noise_green_pollution_sum:.2f}, 倒数阈值={reciprocal_threshold:.1f}, 倒数和超限度={min((noise_green_pollution_sum - reciprocal_threshold) * 0.8, 95):.1f}%"

        # 发送分析结果回主进程 (Global Rank 4)
        result = {'code': type_code, 'detail': analysis_detail}
        comm.send(result, dest=4, tag=200)


    elif rank == 7:
        # 进程7 (原 进程3)：接收 z, w, m 进行环境优化分析
        z = comm.recv(source=4, tag=1, status=status)
        w = comm.recv(source=4, tag=2, status=status)
        m = comm.recv(source=4, tag=3, status=status)

        type_code = 'D0'  # 默认为环境优化平衡
        analysis_detail = ""

        # 条件判断10: if z / (w + 5) < m ** 2
        if z / (w + 5) < m ** 2:
            type_code = 'D1'
            green_coverage = z
            adjusted_pollution_density = w + 5
            green_pollution_regulation_ratio = green_coverage / adjusted_pollution_density
            meteorological_squared_optimization_potential = m ** 2
            optimization_potential_deficit = meteorological_squared_optimization_potential - green_pollution_regulation_ratio
            meteorological_optimization_underutilization = optimization_potential_deficit / green_pollution_regulation_ratio if green_pollution_regulation_ratio > 0 else float(
                'inf')
            weather_optimization_insufficiency = min(meteorological_optimization_underutilization * 33, 95)
            analysis_detail = f"气象优化潜力不足分析: 绿化覆盖={green_coverage}%, 调整污染密度={adjusted_pollution_density:.1f}, 绿化污染调节比={green_pollution_regulation_ratio:.2f}, 气象平方优化潜力={meteorological_squared_optimization_potential:.1f}, 优化潜力缺口={optimization_potential_deficit:.2f}, 气象优化利用不足度={meteorological_optimization_underutilization:.2f}, 天气优化不足度={weather_optimization_insufficiency:.1f}%"

        # 条件判断11: if (z - w) ** 2 > m * 250
        if (z - w) ** 2 > m * 250:
            type_code = 'D2'
            green_coverage = z
            pollution_source_density = w
            green_pollution_difference = green_coverage - pollution_source_density
            environmental_improvement_squared = green_pollution_difference ** 2
            meteorological_regulation_capacity = m * 250
            regulation_capacity_overload = environmental_improvement_squared - meteorological_regulation_capacity
            environmental_improvement_anomaly_ratio = environmental_improvement_squared / meteorological_regulation_capacity if meteorological_regulation_capacity > 0 else float(
                'inf')
            environmental_improvement_distortion = min(environmental_improvement_anomaly_ratio * 26, 95)
            analysis_detail = f"环境改善效果异常分析: 绿化覆盖={green_coverage}%, 污染源密度={pollution_source_density}个/平方公里, 绿化污染差值={green_pollution_difference:.1f}, 环境改善平方={environmental_improvement_squared:.1f}, 气象调节容量={meteorological_regulation_capacity:.1f}, 调节容量过载量={regulation_capacity_overload:.1f}, 环境改善异常比={environmental_improvement_anomaly_ratio:.2f}, 环境改善扭曲度={environmental_improvement_distortion:.1f}%"

        # 条件判断12: if z + w * m > 650
        if z + w * m > 650:
            type_code = 'D3'
            green_coverage = z
            pollution_meteorological_interaction = w * m
            environmental_system_load = green_coverage + pollution_meteorological_interaction
            system_optimization_threshold = 650
            system_load_overflow = environmental_system_load - system_optimization_threshold
            environmental_system_overload_ratio = environmental_system_load / system_optimization_threshold
            system_carrying_capacity_exceedance = min(environmental_system_overload_ratio * 27, 95)
            analysis_detail = f"系统承载阈值超限分析: 绿化覆盖={green_coverage}%, 污染气象交互作用={pollution_meteorological_interaction:.1f}, 环境系统负荷={environmental_system_load:.1f}, 系统优化阈值={system_optimization_threshold}, 系统负荷溢出={system_load_overflow:.1f}, 环境系统过载比={environmental_system_overload_ratio:.2f}, 系统承载能力超限度={system_carrying_capacity_exceedance:.1f}%"
        # 条件判断13: D4
        if z * m > w ** 2 + 100:
            type_code = 'D4'
            green_weather_product = z * m
            pollution_squared_threshold = w ** 2 + 100
            analysis_detail = f"绿化气象积污染超限分析: 绿化气象积={green_weather_product:.2f}, 污染平方阈值={pollution_squared_threshold:.1f}, 积超限度={min((green_weather_product - pollution_squared_threshold) * 0.3, 95):.1f}%"

        # 条件判断14: D5
        if (z + w) / 2 < m * 15 + 50:
            type_code = 'D5'
            green_pollution_average = (z + w) / 2
            weather_multiple_threshold = m * 15 + 50
            analysis_detail = f"平均值收敛状态分析: 绿化污染均值={(z + w) / 2:.2f}, 气象倍数阈值={weather_multiple_threshold:.1f}, 收敛优化度={min((weather_multiple_threshold - green_pollution_average) * 0.5, 95):.1f}%"

        # 条件判断15: D6
        if w ** 2 / 10 > z * m + 80:
            type_code = 'D6'
            pollution_squared_scaled = w ** 2 / 10
            green_weather_product_threshold = z * m + 80
            analysis_detail = f"污染平方气象超限分析: 污染平方缩放={pollution_squared_scaled:.2f}, 绿化气象积阈值={green_weather_product_threshold:.1f}, 平方超限度={min((pollution_squared_scaled - green_weather_product_threshold) * 0.4, 95):.1f}%"

        # 条件判断16: D7
        if z / (m + 1) + w / (m + 2) > 60:
            type_code = 'D7'
            green_pollution_reciprocal_sum = z / (m + 1) + w / (m + 2)
            reciprocal_threshold = 60
            analysis_detail = f"倒数和超限分析: 绿化污染倒数和={green_pollution_reciprocal_sum:.2f}, 倒数阈值={reciprocal_threshold:.1f}, 倒数和超限度={min((green_pollution_reciprocal_sum - reciprocal_threshold) * 1, 95):.1f}%"

        # 发送分析结果回主进程 (Global Rank 4)
        result = {'code': type_code, 'detail': analysis_detail}
        comm.send(result, dest=4, tag=300)

    # -----------------------------------------------------------------
    # --- 程序3：能源消耗分析 (Ranks 8-11) ---
    # -----------------------------------------------------------------
    elif rank == 8:
        # 进程8：主进程 (Global Rank 8)：负责数据生成、分发和宏观能源效率分析

        # 1. 随机生成五个核心能源消耗变量
        x = random.randint(100, 5000)  # 用电负荷 (100-5000 MW)
        y = random.randint(30, 95)  # 节能效率 (30-95%)
        z = random.randint(1, 12)  # 峰值持续时间 (1-12 小时)
        w = random.randint(5, 70)  # 可再生能源比例 (5-70%)
        m = random.randint(1, 10)  # 设备运行状态 (1-10分)

        # 存储数据
        energy_data = [x, y, z, w, m]

        # 2. 分发数据到其他进程 (Ranks 9, 10, 11)
        # 发给进程 9：x, y, z (负荷效率平衡分析)
        comm.send(x, dest=9, tag=1)
        comm.send(y, dest=9, tag=2)
        comm.send(z, dest=9, tag=3)

        # 发给进程 10：y, z, w (可再生能源协调分析)
        comm.send(y, dest=10, tag=1)
        comm.send(z, dest=10, tag=2)
        comm.send(w, dest=10, tag=3)

        # 发给进程 11：z, w, m (能源优化分析)
        comm.send(z, dest=11, tag=1)
        comm.send(w, dest=11, tag=2)
        comm.send(m, dest=11, tag=3)

        # 3. 执行宏观能源效率分析 (xyzwm)
        type_code = 'A0'  # 默认为能源效率平衡状态
        analysis_detail = ""

        # 条件判断1: if x ** 0.5 + y > z * w - 200
        if x ** 0.5 + y > z * w - 200:
            type_code = 'A1'
            power_load_sqrt = x ** 0.5
            energy_efficiency = y
            load_efficiency_sum = power_load_sqrt + energy_efficiency
            peak_renewable_baseline = z * w - 200
            load_regulation_excess = load_efficiency_sum - peak_renewable_baseline
            power_regulation_imbalance = load_regulation_excess / peak_renewable_baseline if peak_renewable_baseline > 0 else float(
                'inf')
            load_adjustment_anomaly = min(power_regulation_imbalance * 32, 100)
            analysis_detail = f"负荷调节异常分析: 电力负荷开方={power_load_sqrt:.2f}MW^0.5, 节能效率={energy_efficiency}%, 负荷效率和={load_efficiency_sum:.2f}, 峰值可再生基准={peak_renewable_baseline:.1f}, 负荷调节超量={load_regulation_excess:.2f}, 功率调节失衡度={power_regulation_imbalance:.2f}, 负荷调节异常度={load_adjustment_anomaly:.1f}%"

        # 条件判断2: if m ** (y // 20) < 50
        if m ** (y // 20) < 50:
            type_code = 'A2'
            equipment_status = m
            efficiency_tier = y // 20 if y >= 20 else 1
            equipment_dynamic_power = m ** efficiency_tier
            operational_baseline_threshold = 50
            equipment_power_deficit = operational_baseline_threshold - equipment_dynamic_power
            equipment_efficiency_mismatch = equipment_power_deficit / equipment_dynamic_power if equipment_dynamic_power > 0 else float(
                'inf')
            equipment_operational_dysfunction = min(equipment_efficiency_mismatch * 38, 95)
            analysis_detail = f"设备效率失配分析: 设备状态={equipment_status}分, 效率档位={efficiency_tier}, 设备动态功率={equipment_dynamic_power:.1f}, 运行基准阈值={operational_baseline_threshold}, 设备功率缺口={equipment_power_deficit:.1f}, 设备效率失配度={equipment_efficiency_mismatch:.2f}, 设备运行功能障碍度={equipment_operational_dysfunction:.1f}%"

        # 条件判断3: if x // 100 + z * m > w + y
        if x // 100 + z * m > w + y:
            type_code = 'A3'
            load_hundred_segment = x // 100
            peak_equipment_interaction = z * m
            comprehensive_energy_demand = load_hundred_segment + peak_equipment_interaction
            renewable_efficiency_sum = w + y
            energy_coordination_imbalance = comprehensive_energy_demand - renewable_efficiency_sum
            comprehensive_energy_incoordination = energy_coordination_imbalance / renewable_efficiency_sum if renewable_efficiency_sum > 0 else float(
                'inf')
            energy_system_disharmony = min(comprehensive_energy_incoordination * 28, 95)
            analysis_detail = f"综合能源不协调分析: 负荷百分段={load_hundred_segment}, 峰值设备交互={peak_equipment_interaction:.1f}, 综合能源需求={comprehensive_energy_demand:.1f}, 可再生效率和={renewable_efficiency_sum:.1f}, 能源协调失衡量={energy_coordination_imbalance:.1f}, 综合能源不协调度={comprehensive_energy_incoordination:.2f}, 能源系统不和谐度={energy_system_disharmony:.1f}%"
        # 条件判断4: A4
        if x / 100 + y > z * w + m * 10:
            type_code = 'A4'
            load_efficiency_sum = x / 100 + y
            peak_renewable_equipment_threshold = z * w + m * 10
            analysis_detail = f"负荷效率峰值可再生和超限分析: 负荷效率和={load_efficiency_sum:.2f}, 峰值可再生设备阈值={peak_renewable_equipment_threshold:.1f}, 和超限度={min((load_efficiency_sum - peak_renewable_equipment_threshold) * 0.3, 95):.1f}%"

        # 条件判断5: A5
        if (x / 100 + y) ** 2 / 100 < z + w + m * 20:
            type_code = 'A5'
            load_efficiency_square_scaled = (x / 100 + y) ** 2 / 100
            peak_renewable_equipment_sum = z + w + m * 20
            analysis_detail = f"综合平方收敛状态分析: 负荷效率平方缩放={(x / 100 + y) ** 2 / 100:.2f}, 峰值可再生设备和={peak_renewable_equipment_sum:.1f}, 收敛优化度={min((peak_renewable_equipment_sum - load_efficiency_square_scaled) * 0.2, 95):.1f}%"

        # 条件判断6: A6
        if x / 1000 + y > z * m + w * 2:
            type_code = 'A6'
            load_efficiency_sum = x / 1000 + y
            peak_equipment_renewable_threshold = z * m + w * 2
            analysis_detail = f"负荷效率和异常分析: 负荷效率和={load_efficiency_sum:.2f}, 峰值设备可再生阈值={peak_equipment_renewable_threshold:.1f}, 和异常度={min((load_efficiency_sum - peak_equipment_renewable_threshold) * 0.5, 95):.1f}%"

        # 4. 收集其他进程的分析结果 (Ranks 9, 10, 11)
        load_efficiency_result = comm.recv(source=9, tag=100, status=status)
        renewable_coordination_result = comm.recv(source=10, tag=200, status=status)
        energy_optimization_result = comm.recv(source=11, tag=300, status=status)

        # 5. 组装完整结果
        analysis_results = [
            f"宏观能源效率 (xyzwm): {type_code} -> {ENERGY_TYPE_DEF.get(type_code, '未知')} | {analysis_detail}",
            f"负荷效率平衡 (xyz): {load_efficiency_result['code']} -> {ENERGY_TYPE_DEF.get(load_efficiency_result['code'], '未知')} | {load_efficiency_result['detail']}",
            f"可再生能源协调 (yzw): {renewable_coordination_result['code']} -> {ENERGY_TYPE_DEF.get(renewable_coordination_result['code'], '未知')} | {renewable_coordination_result['detail']}",
            f"能源优化分析 (zwm): {energy_optimization_result['code']} -> {ENERGY_TYPE_DEF.get(energy_optimization_result['code'], '未知')} | {energy_optimization_result['detail']}"
        ]

        # 6. 打印报告
        print("=" * 70)
        print(f"  能源消耗分析系统 (进程 8-11)  ")
        print("=" * 70)
        print()
        print("--- 实时能源监控数据 ---")
        print(f"用电负荷(X): {x} MW")
        print(f"节能效率(Y): {y}%")
        print(f"峰值持续时间(Z): {z} 小时")
        print(f"可再生能源比例(W): {w}%")
        print(f"设备运行状态(M): {m} 分")
        print()
        print("--- 能源消耗综合分析报告 ---")
        for i, result in enumerate(analysis_results, 1):
            print(f"{i}. {result}")
        print()
        print("=" * 70)
        print(f"程序3 (Ranks 8-11) 分析完成")
        print("=" * 70)
        print("\n")  # 增加间距

    elif rank == 9:
        # 进程9 (原 进程1)：接收 x, y, z 进行负荷效率平衡分析
        x = comm.recv(source=8, tag=1, status=status)
        y = comm.recv(source=8, tag=2, status=status)
        z = comm.recv(source=8, tag=3, status=status)

        type_code = 'B0'  # 默认为负荷效率平衡
        analysis_detail = ""

        # 条件判断4: if (x * y) ** (z // 4) > 500000
        if (x * y) ** (z // 4) > 500000:
            type_code = 'B1'
            load_efficiency_product = x * y
            peak_tier_exponent = z // 4 if z >= 4 else 1
            dynamic_power_amplification = (x * y) ** peak_tier_exponent
            power_carrying_threshold = 500000
            dynamic_power_overload = dynamic_power_amplification - power_carrying_threshold
            power_amplification_factor = dynamic_power_amplification / power_carrying_threshold
            dynamic_power_saturation = min(power_amplification_factor * 15, 95)
            analysis_detail = f"动态功率超载分析: 负荷效率乘积={load_efficiency_product}, 峰值档位指数={peak_tier_exponent}, 动态功率放大={dynamic_power_amplification:.1f}, 功率承载阈值={power_carrying_threshold}, 动态功率过载量={dynamic_power_overload:.1f}, 功率放大因子={power_amplification_factor:.2f}, 动态功率饱和度={dynamic_power_saturation:.1f}%"

        # 条件判断5: if x % (y + z) > 100
        if x % (y + z) > 100:
            type_code = 'B2'
            power_load = x
            efficiency_peak_sum = y + z
            load_modular_remainder = x % efficiency_peak_sum if efficiency_peak_sum > 0 else 0
            power_fluctuation_threshold = 100
            load_fluctuation_excess = load_modular_remainder - power_fluctuation_threshold
            power_fluctuation_intensity = load_fluctuation_excess / power_fluctuation_threshold if power_fluctuation_threshold > 0 else 0
            electrical_fluctuation_anomaly = min(power_fluctuation_intensity * 42, 95)
            analysis_detail = f"电力波动异常分析: 电力负荷={power_load}MW, 效率峰值和={efficiency_peak_sum:.1f}, 负荷模数余数={load_modular_remainder:.1f}, 功率波动阈值={power_fluctuation_threshold}, 负荷波动超量={load_fluctuation_excess:.1f}, 功率波动强度={power_fluctuation_intensity:.2f}, 电力波动异常度={electrical_fluctuation_anomaly:.1f}%"

        # 条件判断6: if x ** 2 - y * z > 8000
        if x ** 2 - y * z > 8000:
            type_code = 'B3'
            load_squared_power = x ** 2
            efficiency_peak_product = y * z
            power_gap_magnitude = load_squared_power - efficiency_peak_product
            system_power_shortage_threshold = 8000
            power_shortage_excess = power_gap_magnitude - system_power_shortage_threshold
            power_gap_severity_ratio = power_shortage_excess / system_power_shortage_threshold if system_power_shortage_threshold > 0 else 0
            system_power_deficit_criticality = min(power_gap_severity_ratio * 25, 95)
            analysis_detail = f"系统功率缺口过大分析: 负荷平方功率={load_squared_power}, 效率峰值乘积={efficiency_peak_product:.1f}, 功率缺口幅度={power_gap_magnitude:.1f}, 系统功率短缺阈值={system_power_shortage_threshold}, 功率短缺超量={power_shortage_excess:.1f}, 功率缺口严重性比={power_gap_severity_ratio:.2f}, 系统功率缺口临界度={system_power_deficit_criticality:.1f}%"
        # 条件判断7: B4
        if x / 100 + y > z ** 2 + 50:
            type_code = 'B4'
            load_efficiency_sum = x / 100 + y
            peak_squared_threshold = z ** 2 + 50
            analysis_detail = f"负荷效率和峰值超限分析: 负荷效率和={load_efficiency_sum:.2f}, 峰值平方阈值={peak_squared_threshold:.1f}, 和超限度={min((load_efficiency_sum - peak_squared_threshold) * 0.25, 95):.1f}%"

        # 条件判断8: B5
        if (x / 100 + y) / 2 > z * 8 + 40:
            type_code = 'B5'
            load_efficiency_average = (x / 100 + y) / 2
            peak_multiple_threshold = z * 8 + 40
            analysis_detail = f"平均值峰值失衡分析: 负荷效率均值={(x / 100 + y) / 2:.2f}, 峰值倍数阈值={peak_multiple_threshold:.1f}, 平均失衡度={min((load_efficiency_average - peak_multiple_threshold) * 0.5, 95):.1f}%"

        # 条件判断9: B6
        if x / 1000 + y > z * 10 + 60:
            type_code = 'B6'
            load_efficiency_sum = x / 1000 + y
            peak_multiple_threshold = z * 10 + 60
            analysis_detail = f"负荷效率和峰值异常分析: 负荷效率和={load_efficiency_sum:.2f}, 峰值倍数阈值={peak_multiple_threshold:.1f}, 和异常度={min((load_efficiency_sum - peak_multiple_threshold) * 0.6, 95):.1f}%"

        # 条件判断10: B7
        if x / (z + 1) > y * 20:
            type_code = 'B7'
            load_peak_reciprocal = x / (z + 1)
            efficiency_threshold = y * 20
            analysis_detail = f"负荷峰值倒数超限分析: 负荷峰值倒数={load_peak_reciprocal:.2f}, 效率阈值={efficiency_threshold:.1f}, 倒数超限度={min((load_peak_reciprocal - efficiency_threshold) * 0.015, 95):.1f}%"

        # 发送分析结果回主进程 (Global Rank 8)
        result = {'code': type_code, 'detail': analysis_detail}
        comm.send(result, dest=8, tag=100)


    elif rank == 10:
        # 进程10 (原 进程2)：接收 y, z, w 进行可再生能源协调分析
        y = comm.recv(source=8, tag=1, status=status)
        z = comm.recv(source=8, tag=2, status=status)
        w = comm.recv(source=8, tag=3, status=status)

        type_code = 'C0'  # 默认为可再生能源协调
        analysis_detail = ""

        # 条件判断7: if y ** (w // 15) < z * 20
        if y ** (w // 15) < z * 20:
            type_code = 'C1'
            energy_efficiency = y
            renewable_tier_exponent = w // 15 if w >= 15 else 1
            efficiency_renewable_power = y ** renewable_tier_exponent
            peak_regulation_capacity = z * 20
            clean_energy_regulation_deficit = peak_regulation_capacity - efficiency_renewable_power
            renewable_regulation_insufficiency = clean_energy_regulation_deficit / efficiency_renewable_power if efficiency_renewable_power > 0 else float(
                'inf')
            clean_energy_adjustment_inadequacy = min(renewable_regulation_insufficiency * 35, 95)
            analysis_detail = f"清洁能源调节不足分析: 节能效率={energy_efficiency}%, 可再生档位指数={renewable_tier_exponent}, 效率可再生功率={efficiency_renewable_power:.1f}, 峰值调节容量={peak_regulation_capacity:.1f}, 清洁能源调节缺口={clean_energy_regulation_deficit:.1f}, 可再生调节不足度={renewable_regulation_insufficiency:.2f}, 清洁能源调节不足度={clean_energy_adjustment_inadequacy:.1f}%"

        # 条件判断8: if (y + w) ** 0.5 > z + 30
        if (y + w) ** 0.5 > z + 30:
            type_code = 'C2'
            efficiency_renewable_sum = y + w
            energy_composite_sqrt = (y + w) ** 0.5
            peak_regulation_threshold = z + 30
            regulation_threshold_overload = energy_composite_sqrt - peak_regulation_threshold
            energy_regulation_overflow_ratio = regulation_threshold_overload / peak_regulation_threshold if peak_regulation_threshold > 0 else 0
            energy_regulation_threshold_exceedance = min(energy_regulation_overflow_ratio * 30, 95)
            analysis_detail = f"能源调节阈值超限分析: 效率可再生和={efficiency_renewable_sum:.1f}, 能源复合开方={energy_composite_sqrt:.2f}, 峰值调节阈值={peak_regulation_threshold:.1f}, 调节阈值过载量={regulation_threshold_overload:.2f}, 能源调节溢出比={energy_regulation_overflow_ratio:.2f}, 能源调节阈值超限度={energy_regulation_threshold_exceedance:.1f}%"

        # 条件判断9: if y * w // 10 == z * 3
        if y * w // 10 == z * 3:
            type_code = 'C3'
            efficiency_renewable_product = y * w
            efficiency_renewable_segment = y * w // 10
            peak_triple_target = z * 3
            perfect_match_indicator = 1 if efficiency_renewable_segment == peak_triple_target else 0
            energy_matching_deviation = abs(efficiency_renewable_segment - peak_triple_target)
            perfect_energy_synchronization_anomaly = perfect_match_indicator * 88 + (
                        10 - min(energy_matching_deviation, 10)) * 2
            analysis_detail = f"完美能源匹配异常分析: 效率可再生乘积={efficiency_renewable_product}, 效率可再生分段={efficiency_renewable_segment:.1f}, 峰值三倍目标={peak_triple_target:.1f}, 完美匹配指示={perfect_match_indicator}, 能源匹配偏差={energy_matching_deviation:.1f}, 完美能源同步异常度={perfect_energy_synchronization_anomaly:.1f}%"
        # 条件判断10: C4
        if y + w > z ** 2 + 80:
            type_code = 'C4'
            efficiency_renewable_sum = y + w
            peak_squared_threshold = z ** 2 + 80
            analysis_detail = f"效率可再生和峰值超限分析: 效率可再生和={efficiency_renewable_sum:.1f}, 峰值平方阈值={peak_squared_threshold:.1f}, 和超限度={min((efficiency_renewable_sum - peak_squared_threshold) * 0.4, 95):.1f}%"

        # 条件判断11: C5
        if (y + w) ** 2 / 100 < z * 6 + 60:
            type_code = 'C5'
            efficiency_renewable_square_scaled = (y + w) ** 2 / 100
            peak_multiple_threshold = z * 6 + 60
            analysis_detail = f"平方和收敛状态分析: 效率可再生平方缩放={(y + w) ** 2 / 100:.2f}, 峰值倍数阈值={peak_multiple_threshold:.1f}, 收敛优化度={min((peak_multiple_threshold - efficiency_renewable_square_scaled) * 0.25, 95):.1f}%"

        # 条件判断12: C6
        if w / (z + 1) + y > 70:
            type_code = 'C6'
            renewable_peak_efficiency_sum = w / (z + 1) + y
            reciprocal_threshold = 70
            analysis_detail = f"倒数和超限分析: 可再生峰值效率和={renewable_peak_efficiency_sum:.2f}, 倒数阈值={reciprocal_threshold:.1f}, 倒数和超限度={min((renewable_peak_efficiency_sum - reciprocal_threshold) * 1, 95):.1f}%"

        # 发送分析结果回主进程 (Global Rank 8)
        result = {'code': type_code, 'detail': analysis_detail}
        comm.send(result, dest=8, tag=200)


    elif rank == 11:
        # 进程11 (原 进程3)：接收 z, w, m 进行能源优化分析
        z = comm.recv(source=8, tag=1, status=status)
        w = comm.recv(source=8, tag=2, status=status)
        m = comm.recv(source=8, tag=3, status=status)

        type_code = 'D0'  # 默认为能源优化平衡
        analysis_detail = ""

        # 条件判断10: if z ** (m // 2) > w * 100
        if z ** (m // 2) > w * 100:
            type_code = 'D1'
            peak_duration = z
            equipment_tier_exponent = m // 2 if m >= 2 else 1
            peak_equipment_exponential_power = z ** equipment_tier_exponent
            renewable_hundred_baseline = w * 100
            peak_power_overload = peak_equipment_exponential_power - renewable_hundred_baseline
            peak_equipment_power_amplification = peak_equipment_exponential_power / renewable_hundred_baseline if renewable_hundred_baseline > 0 else float(
                'inf')
            peak_equipment_power_saturation = min(peak_equipment_power_amplification * 22, 95)
            analysis_detail = f"峰值设备功率超载分析: 峰值持续时间={peak_duration}小时, 设备档位指数={equipment_tier_exponent}, 峰值设备指数功率={peak_equipment_exponential_power:.1f}, 可再生百倍基准={renewable_hundred_baseline:.1f}, 峰值功率过载量={peak_power_overload:.1f}, 峰值设备功率放大度={peak_equipment_power_amplification:.2f}, 峰值设备功率饱和度={peak_equipment_power_saturation:.1f}%"

        # 条件判断11: if (z * w) ** 0.5 + m > 85
        if (z * w) ** 0.5 + m > 85:
            type_code = 'D2'
            peak_renewable_product = z * w
            peak_renewable_sqrt = (z * w) ** 0.5
            equipment_status = m
            system_optimization_composite = peak_renewable_sqrt + equipment_status
            system_optimization_threshold = 85
            optimization_threshold_overflow = system_optimization_composite - system_optimization_threshold
            system_optimization_overload_ratio = optimization_threshold_overflow / system_optimization_threshold if system_optimization_threshold > 0 else 0
            system_optimization_exceedance = min(system_optimization_overload_ratio * 33, 95)
            analysis_detail = f"系统优化阈值超限分析: 峰值可再生乘积={peak_renewable_product:.1f}, 峰值可再生开方={peak_renewable_sqrt:.2f}, 设备状态={equipment_status}分, 系统优化复合值={system_optimization_composite:.2f}, 系统优化阈值={system_optimization_threshold}, 优化阈值溢出={optimization_threshold_overflow:.2f}, 系统优化过载比={system_optimization_overload_ratio:.2f}, 系统优化超限度={system_optimization_exceedance:.1f}%"

        # 条件判断12: if z * m % (w + 10) < 5
        if z * m % (w + 10) < 5:
            type_code = 'D3'
            peak_equipment_product = z * m
            renewable_adjusted_divisor = w + 10
            energy_synchronization_remainder = peak_equipment_product % renewable_adjusted_divisor
            energy_sync_threshold = 5
            synchronization_margin = energy_sync_threshold - energy_synchronization_remainder
            energy_synchronization_precision = (
                                                           energy_sync_threshold - energy_synchronization_remainder) / energy_sync_threshold * 100
            energy_synchronization_anomaly_level = min(energy_synchronization_precision, 90)
            analysis_detail = f"能源同步异常分析: 峰值设备乘积={peak_equipment_product:.1f}, 可再生调整除数={renewable_adjusted_divisor:.1f}, 能源同步余数={energy_synchronization_remainder:.1f}, 能源同步阈值={energy_sync_threshold}, 同步边际={synchronization_margin:.1f}, 能源同步精度={energy_synchronization_precision:.1f}%, 能源同步异常水平={energy_synchronization_anomaly_level:.1f}%"
        # 条件判断13: D4
        if z * w / 10 > m ** 2 + 50:
            type_code = 'D4'
            peak_renewable_product_scaled = z * w / 10
            equipment_squared_threshold = m ** 2 + 50
            analysis_detail = f"峰值可再生积设备超限分析: 峰值可再生积缩放={peak_renewable_product_scaled:.2f}, 设备平方阈值={equipment_squared_threshold:.1f}, 积超限度={min((peak_renewable_product_scaled - equipment_squared_threshold) * 0.5, 95):.1f}%"

        # 条件判断14: D5
        if (z + w) / 2 < m * 10 + 30:
            type_code = 'D5'
            peak_renewable_average = (z + w) / 2
            equipment_multiple_threshold = m * 10 + 30
            analysis_detail = f"平均值收敛状态分析: 峰值可再生均值={(z + w) / 2:.2f}, 设备倍数阈值={equipment_multiple_threshold:.1f}, 收敛优化度={min((equipment_multiple_threshold - peak_renewable_average) * 0.8, 95):.1f}%"

        # 发送分析结果回主进程 (Global Rank 8)
        result = {'code': type_code, 'detail': analysis_detail}
        comm.send(result, dest=8, tag=300)

    # -----------------------------------------------------------------
    # --- 程序4：公共安全评估分析 (Ranks 12-15) ---
    # -----------------------------------------------------------------
    elif rank == 12:
        # 进程12：主进程 (Global Rank 12)：负责数据生成、分发和宏观公共安全分析

        # 1. 随机生成五个核心公共安全变量
        x = random.randint(5, 60)  # 事件响应时间 (5-60 分钟)
        y = random.randint(40, 100)  # 警力覆盖率 (40-100%)
        z = random.randint(10, 200)  # 监控密度 (10-200 个/平方公里)
        w = random.randint(30, 95)  # 市民安全感 (30-95%)
        m = random.randint(1, 10)  # 设施完善度 (1-10分)

        # 存储数据
        safety_data = [x, y, z, w, m]

        # 2. 分发数据到其他进程 (Ranks 13, 14, 15)
        # 发给进程 13：x, y, z (安全响应协调分析)
        comm.send(x, dest=13, tag=1)
        comm.send(y, dest=13, tag=2)
        comm.send(z, dest=13, tag=3)

        # 发给进程 14：y, z, w (警力监控协调分析)
        comm.send(y, dest=14, tag=1)
        comm.send(z, dest=14, tag=2)
        comm.send(w, dest=14, tag=3)

        # 发给进程 15：z, w, m (安全优化分析)
        comm.send(z, dest=15, tag=1)
        comm.send(w, dest=15, tag=2)
        comm.send(m, dest=15, tag=3)

        # 3. 执行宏观公共安全分析 (xyzwm)
        type_code = 'A0'  # 默认为公共安全平衡状态
        analysis_detail = ""

        # 条件判断1: if x / y + z / w > m + 15
        if x / y + z / w > m + 15:
            type_code = 'A1'
            response_police_ratio = x / y if y > 0 else 0
            monitoring_safety_ratio = z / w if w > 0 else 0
            fractional_combination = response_police_ratio + monitoring_safety_ratio
            facility_baseline_threshold = m + 15
            fractional_coordination_excess = fractional_combination - facility_baseline_threshold
            fractional_imbalance_factor = fractional_coordination_excess / facility_baseline_threshold if facility_baseline_threshold > 0 else 0
            fractional_coordination_anomaly = min(fractional_imbalance_factor * 28, 95)
            analysis_detail = f"分式协调异常分析: 响应警力比={response_police_ratio:.2f}, 监控安全感比={monitoring_safety_ratio:.2f}, 分式组合值={fractional_combination:.2f}, 设施基线阈值={facility_baseline_threshold:.1f}, 分式协调超量={fractional_coordination_excess:.2f}, 分式失衡因子={fractional_imbalance_factor:.2f}, 分式协调异常度={fractional_coordination_anomaly:.1f}%"

        # 条件判断2: if (x + y) / (z + w) < m * 0.8
        if (x + y) / (z + w) < m * 0.8:
            type_code = 'A2'
            response_police_sum = x + y
            monitoring_safety_sum = z + w
            proportional_coordination_ratio = response_police_sum / monitoring_safety_sum if monitoring_safety_sum > 0 else 0
            facility_proportional_standard = m * 0.8
            proportional_coordination_deficit = facility_proportional_standard - proportional_coordination_ratio
            proportional_insufficiency_factor = proportional_coordination_deficit / proportional_coordination_ratio if proportional_coordination_ratio > 0 else float(
                'inf')
            proportional_coordination_inadequacy = min(proportional_insufficiency_factor * 35, 95)
            analysis_detail = f"比例协调不足分析: 响应警力和={response_police_sum:.1f}, 监控安全感和={monitoring_safety_sum:.1f}, 比例协调比={proportional_coordination_ratio:.2f}, 设施比例标准={facility_proportional_standard:.2f}, 比例协调缺口={proportional_coordination_deficit:.2f}, 比例不足因子={proportional_insufficiency_factor:.2f}, 比例协调不足度={proportional_coordination_inadequacy:.1f}%"

        # 条件判断3: if x ** 3 + y ** 2 + z > w * m + 8000
        if x ** 3 + y ** 2 + z > w * m + 8000:
            type_code = 'A3'
            response_cubic_component = x ** 3
            police_quadratic_component = y ** 2
            monitoring_linear_component = z
            polynomial_safety_aggregate = response_cubic_component + police_quadratic_component + monitoring_linear_component
            safety_facility_baseline = w * m + 8000
            polynomial_overload_excess = polynomial_safety_aggregate - safety_facility_baseline
            polynomial_safety_saturation = polynomial_overload_excess / safety_facility_baseline if safety_facility_baseline > 0 else 0
            polynomial_safety_stress = min(polynomial_safety_saturation * 22, 95)
            analysis_detail = f"多项式安全超载分析: 响应立方分量={response_cubic_component}, 警力二次分量={police_quadratic_component}, 监控线性分量={monitoring_linear_component}, 多项式安全聚合={polynomial_safety_aggregate:.1f}, 安全设施基线={safety_facility_baseline:.1f}, 多项式过载超量={polynomial_overload_excess:.1f}, 多项式安全饱和度={polynomial_safety_saturation:.2f}, 多项式安全压力={polynomial_safety_stress:.1f}%"
        # 条件判断4: A4
        if x + y > z + w + m * 10:
            type_code = 'A4'
            response_police_sum = x + y
            monitoring_safety_facility_threshold = z + w + m * 10
            analysis_detail = f"响应警力监控安全和超限分析: 响应警力和={response_police_sum:.1f}, 监控安全设施阈值={monitoring_safety_facility_threshold:.1f}, 和超限度={min((response_police_sum - monitoring_safety_facility_threshold) * 0.5, 95):.1f}%"

        # 条件判断5: A5
        if (x + y) ** 2 / 100 < z / 10 + w + m * 5:
            type_code = 'A5'
            response_police_square_scaled = (x + y) ** 2 / 100
            monitoring_safety_facility_sum = z / 10 + w + m * 5
            analysis_detail = f"综合平方收敛状态分析: 响应警力平方缩放={(x + y) ** 2 / 100:.2f}, 监控安全设施和={monitoring_safety_facility_sum:.1f}, 收敛优化度={min((monitoring_safety_facility_sum - response_police_square_scaled) * 0.3, 95):.1f}%"

        # 4. 收集其他进程的分析结果 (Ranks 13, 14, 15)
        response_coordination_result = comm.recv(source=13, tag=100, status=status)
        police_monitoring_result = comm.recv(source=14, tag=200, status=status)
        safety_optimization_result = comm.recv(source=15, tag=300, status=status)

        # 5. 组装完整结果
        analysis_results = [
            f"宏观公共安全 (xyzwm): {type_code} -> {SAFETY_TYPE_DEF.get(type_code, '未知')} | {analysis_detail}",
            f"安全响应协调 (xyz): {response_coordination_result['code']} -> {SAFETY_TYPE_DEF.get(response_coordination_result['code'], '未知')} | {response_coordination_result['detail']}",
            f"警力监控协调 (yzw): {police_monitoring_result['code']} -> {SAFETY_TYPE_DEF.get(police_monitoring_result['code'], '未知')} | {police_monitoring_result['detail']}",
            f"安全优化分析 (zwm): {safety_optimization_result['code']} -> {SAFETY_TYPE_DEF.get(safety_optimization_result['code'], '未知')} | {safety_optimization_result['detail']}"
        ]

        # 6. 打印报告
        print("=" * 70)
        print(f"  公共安全评估系统 (进程 12-15)  ")
        print("=" * 70)
        print()
        print("--- 实时公共安全数据 ---")
        print(f"事件响应时间(X): {x} 分钟")
        print(f"警力覆盖率(Y): {y}%")
        print(f"监控密度(Z): {z} 个/平方公里")
        print(f"市民安全感(W): {w}%")
        print(f"设施完善度(M): {m} 分")
        print()
        print("--- 公共安全综合分析报告 ---")
        for i, result in enumerate(analysis_results, 1):
            print(f"{i}. {result}")
        print()
        print("=" * 70)
        print(f"程序4 (Ranks 12-15) 分析完成")
        print("=" * 70)
        print("\n")  # 增加间距

    elif rank == 13:
        # 进程13 (原 进程1)：接收 x, y, z 进行安全响应协调分析
        x = comm.recv(source=12, tag=1, status=status)
        y = comm.recv(source=12, tag=2, status=status)
        z = comm.recv(source=12, tag=3, status=status)

        type_code = 'B0'  # 默认为安全响应协调
        analysis_detail = ""

        # 条件判断4: if x / (y / z) > 120
        if x / (y / z) > 120:
            type_code = 'B1'
            response_time = x
            police_monitoring_ratio = y / z if z > 0 else 1
            nested_division_result = x / police_monitoring_ratio if police_monitoring_ratio > 0 else 0
            nested_division_threshold = 120
            nested_response_excess = nested_division_result - nested_division_threshold
            nested_response_amplification = nested_response_excess / nested_division_threshold if nested_division_threshold > 0 else 0
            nested_response_dysfunction = min(nested_response_amplification * 33, 95)
            analysis_detail = f"嵌套响应异常分析: 响应时间={response_time}分钟, 警力监控比={police_monitoring_ratio:.2f}, 嵌套除法结果={nested_division_result:.2f}, 嵌套除法阈值={nested_division_threshold}, 嵌套响应超量={nested_response_excess:.2f}, 嵌套响应放大度={nested_response_amplification:.2f}, 嵌套响应功能障碍度={nested_response_dysfunction:.1f}%"

        # 条件判断5: if (x * z) % (y + 5) > 20
        if (x * z) % (y + 5) > 20:
            type_code = 'B2'
            response_monitoring_product = x * z
            police_adjusted_divisor = y + 5
            product_modular_remainder = response_monitoring_product % police_adjusted_divisor
            modular_threshold = 20
            modular_excess = product_modular_remainder - modular_threshold
            product_modular_anomaly_ratio = modular_excess / modular_threshold if modular_threshold > 0 else 0
            product_modular_dysfunction = min(product_modular_anomaly_ratio * 40, 95)
            analysis_detail = f"乘积模运算异常分析: 响应监控乘积={response_monitoring_product}, 警力调整除数={police_adjusted_divisor:.1f}, 乘积模数余数={product_modular_remainder:.1f}, 模运算阈值={modular_threshold}, 模数超量={modular_excess:.1f}, 乘积模数异常比={product_modular_anomaly_ratio:.2f}, 乘积模数功能障碍度={product_modular_dysfunction:.1f}%"

        # 条件判断6: if x ** 2 + z ** 2 < y * 50
        if x ** 2 + z ** 2 < y * 50:
            type_code = 'B3'
            response_squared = x ** 2
            monitoring_squared = z ** 2
            response_monitoring_square_sum = response_squared + monitoring_squared
            police_fifty_baseline = y * 50
            square_sum_deficit = police_fifty_baseline - response_monitoring_square_sum
            square_sum_insufficiency_ratio = square_sum_deficit / response_monitoring_square_sum if response_monitoring_square_sum > 0 else 0
            response_monitoring_square_inadequacy = min(square_sum_insufficiency_ratio * 30, 95)
            analysis_detail = f"响应监控平方不足分析: 响应时间平方={response_squared}, 监控密度平方={monitoring_squared}, 响应监控平方和={response_monitoring_square_sum:.1f}, 警力50倍基线={police_fifty_baseline:.1f}, 平方和缺口={square_sum_deficit:.1f}, 平方和不足比={square_sum_insufficiency_ratio:.2f}, 响应监控平方不足度={response_monitoring_square_inadequacy:.1f}%"
        # 条件判断7: B4
        if x * y / 10 > z + 100:
            type_code = 'B4'
            response_police_product_scaled = x * y / 10
            monitoring_threshold = z + 100
            analysis_detail = f"响应警力积监控超限分析: 响应警力积缩放={response_police_product_scaled:.2f}, 监控阈值={monitoring_threshold:.1f}, 积超限度={min((response_police_product_scaled - monitoring_threshold) * 0.3, 95):.1f}%"

        # 条件判断8: B5
        if (x + y) / 2 > z / 5 + 50:
            type_code = 'B5'
            response_police_average = (x + y) / 2
            monitoring_threshold = z / 5 + 50
            analysis_detail = f"平均值监控失衡分析: 响应警力均值={(x + y) / 2:.2f}, 监控阈值={monitoring_threshold:.1f}, 平均失衡度={min((response_police_average - monitoring_threshold) * 0.8, 95):.1f}%"

        # 条件判断9: B6
        if x ** 2 / 10 + y > z + 120:
            type_code = 'B6'
            response_squared_police_sum = x ** 2 / 10 + y
            monitoring_threshold = z + 120
            analysis_detail = f"平方和监控异常分析: 响应平方警力和={response_squared_police_sum:.2f}, 监控阈值={monitoring_threshold:.1f}, 平方和异常度={min((response_squared_police_sum - monitoring_threshold) * 0.4, 95):.1f}%"

        # 发送分析结果回主进程 (Global Rank 12)
        result = {'code': type_code, 'detail': analysis_detail}
        comm.send(result, dest=12, tag=100)


    elif rank == 14:
        # 进程14 (原 进程2)：接收 y, z, w 进行警力监控协调分析
        y = comm.recv(source=12, tag=1, status=status)
        z = comm.recv(source=12, tag=2, status=status)
        w = comm.recv(source=12, tag=3, status=status)

        type_code = 'C0'  # 默认为警力监控协调
        analysis_detail = ""

        # 条件判断7: if y / z + w / 10 > 8
        if y / z + w / 10 > 8:
            type_code = 'C1'
            police_monitoring_ratio = y / z if z > 0 else 0
            safety_tenth_component = w / 10
            fractional_police_combination = police_monitoring_ratio + safety_tenth_component
            fractional_police_threshold = 8
            fractional_police_excess = fractional_police_combination - fractional_police_threshold
            fractional_police_overload_factor = fractional_police_excess / fractional_police_threshold if fractional_police_threshold > 0 else 0
            fractional_police_saturation = min(fractional_police_overload_factor * 31, 95)
            analysis_detail = f"分式警力超载分析: 警力监控比={police_monitoring_ratio:.2f}, 安全感十分之一={safety_tenth_component:.2f}, 分式警力组合={fractional_police_combination:.2f}, 分式警力阈值={fractional_police_threshold}, 分式警力超量={fractional_police_excess:.2f}, 分式警力过载因子={fractional_police_overload_factor:.2f}, 分式警力饱和度={fractional_police_saturation:.1f}%"

        # 条件判断8: if (y + w) / z < 3
        if (y + w) / z < 3:
            type_code = 'C2'
            police_safety_sum = y + w
            monitoring_density = z
            police_safety_monitoring_ratio = police_safety_sum / monitoring_density if monitoring_density > 0 else 0
            proportional_threshold = 3
            proportional_deficit = proportional_threshold - police_safety_monitoring_ratio
            police_monitoring_proportional_insufficiency = proportional_deficit / police_safety_monitoring_ratio if police_safety_monitoring_ratio > 0 else float(
                'inf')
            police_monitoring_proportional_imbalance = min(police_monitoring_proportional_insufficiency * 37, 95)
            analysis_detail = f"警力监控比例失调分析: 警力安全感和={police_safety_sum:.1f}, 监控密度={monitoring_density}, 警力安全监控比={police_safety_monitoring_ratio:.2f}, 比例阈值={proportional_threshold}, 比例缺口={proportional_deficit:.2f}, 警力监控比例不足度={police_monitoring_proportional_insufficiency:.2f}, 警力监控比例失衡度={police_monitoring_proportional_imbalance:.1f}%"

        # 条件判断9: if y * w % (z // 5) == 0
        if y * w % (z // 5) == 0:
            type_code = 'C3'
            police_safety_product = y * w
            monitoring_five_segment = z // 5 if z >= 5 else 1
            perfect_coordination_remainder = police_safety_product % monitoring_five_segment
            perfect_match_indicator = 1 if perfect_coordination_remainder == 0 else 0
            coordination_deviation = abs(perfect_coordination_remainder - 0)
            perfect_coordination_anomaly_score = perfect_match_indicator * 92 + (
                        5 - min(coordination_deviation, 5)) * 1.5
            analysis_detail = f"完美协调匹配异常分析: 警力安全感乘积={police_safety_product}, 监控五分段={monitoring_five_segment}, 完美协调余数={perfect_coordination_remainder:.1f}, 完美匹配指示={perfect_match_indicator}, 协调偏差={coordination_deviation:.1f}, 完美协调异常评分={perfect_coordination_anomaly_score:.1f}%"
        # 条件判断10: C4
        if y + w > z + 150:
            type_code = 'C4'
            police_safety_sum = y + w
            monitoring_threshold = z + 150
            analysis_detail = f"警力安全和监控超限分析: 警力安全和={police_safety_sum:.1f}, 监控阈值={monitoring_threshold:.1f}, 和超限度={min((police_safety_sum - monitoring_threshold) * 0.5, 95):.1f}%"

        # 条件判断11: C5
        if (y + w) ** 2 / 100 < z / 5 + 50:
            type_code = 'C5'
            police_safety_square_scaled = (y + w) ** 2 / 100
            monitoring_threshold = z / 5 + 50
            analysis_detail = f"平方和收敛状态分析: 警力安全平方缩放={(y + w) ** 2 / 100:.2f}, 监控阈值={monitoring_threshold:.1f}, 收敛优化度={min((monitoring_threshold - police_safety_square_scaled) * 0.25, 95):.1f}%"

        # 条件判断12: C6
        if w / (z + 1) + y / 10 > 15:
            type_code = 'C6'
            safety_monitoring_police_sum = w / (z + 1) + y / 10
            reciprocal_threshold = 15
            analysis_detail = f"倒数和超限分析: 安全监控警力和={safety_monitoring_police_sum:.2f}, 倒数阈值={reciprocal_threshold:.1f}, 倒数和超限度={min((safety_monitoring_police_sum - reciprocal_threshold) * 3, 95):.1f}%"

        # 条件判断13: C7
        if y ** 2 / 100 + w > z / 5 + 120:
            type_code = 'C7'
            police_squared_safety_sum = y ** 2 / 100 + w
            monitoring_threshold = z / 5 + 120
            analysis_detail = f"平方和监控异常分析: 警力平方安全和={police_squared_safety_sum:.2f}, 监控阈值={monitoring_threshold:.1f}, 平方和异常度={min((police_squared_safety_sum - monitoring_threshold) * 0.3, 95):.1f}%"

        # 发送分析结果回主进程 (Global Rank 12)
        result = {'code': type_code, 'detail': analysis_detail}
        comm.send(result, dest=12, tag=200)


    elif rank == 15:
        # 进程15 (原 进程3)：接收 z, w, m 进行安全优化分析
        z = comm.recv(source=12, tag=1, status=status)
        w = comm.recv(source=12, tag=2, status=status)
        m = comm.recv(source=12, tag=3, status=status)

        type_code = 'D0'  # 默认为安全优化平衡
        analysis_detail = ""

        # 条件判断10: if z / w * m > 50
        if z / w * m > 50:
            type_code = 'D1'
            monitoring_safety_ratio = z / w if w > 0 else 0
            facility_completeness = m
            continuous_operation_result = monitoring_safety_ratio * facility_completeness
            continuous_operation_threshold = 50
            continuous_operation_excess = continuous_operation_result - continuous_operation_threshold
            continuous_operation_amplification = continuous_operation_excess / continuous_operation_threshold if continuous_operation_threshold > 0 else 0
            continuous_operation_saturation = min(continuous_operation_amplification * 26, 95)
            analysis_detail = f"连续运算超载分析: 监控安全感比={monitoring_safety_ratio:.2f}, 设施完善度={facility_completeness}分, 连续运算结果={continuous_operation_result:.2f}, 连续运算阈值={continuous_operation_threshold}, 连续运算超量={continuous_operation_excess:.2f}, 连续运算放大度={continuous_operation_amplification:.2f}, 连续运算饱和度={continuous_operation_saturation:.1f}%"

        # 条件判断11: if (z + m) ** 2 / w > 80
        if (z + m) ** 2 / w > 80:
            type_code = 'D2'
            monitoring_facility_sum = z + m
            monitoring_facility_squared = (z + m) ** 2
            safety_feeling = w
            square_division_result = monitoring_facility_squared / safety_feeling if safety_feeling > 0 else 0
            square_division_threshold = 80
            square_division_excess = square_division_result - square_division_threshold
            square_division_anomaly_ratio = square_division_excess / square_division_threshold if square_division_threshold > 0 else 0
            square_division_dysfunction = min(square_division_anomaly_ratio * 24, 95)
            analysis_detail = f"平方除法异常分析: 监控设施和={monitoring_facility_sum:.1f}, 监控设施平方={monitoring_facility_squared:.1f}, 安全感={safety_feeling}%, 平方除法结果={square_division_result:.2f}, 平方除法阈值={square_division_threshold}, 平方除法超量={square_division_excess:.2f}, 平方除法异常比={square_division_anomaly_ratio:.2f}, 平方除法功能障碍度={square_division_dysfunction:.1f}%"

        # 条件判断12: if z % m + w % m > 15
        if z % m + w % m > 15:
            type_code = 'D3'
            monitoring_facility_remainder = z % m if m > 0 else 0
            safety_facility_remainder = w % m if m > 0 else 0
            multiple_modular_sum = monitoring_facility_remainder + safety_facility_remainder
            multiple_modular_threshold = 15
            multiple_modular_excess = multiple_modular_sum - multiple_modular_threshold
            multiple_modular_anomaly_factor = multiple_modular_excess / multiple_modular_threshold if multiple_modular_threshold > 0 else 0
            multiple_modular_dysfunction = min(multiple_modular_anomaly_factor * 38, 95)
            analysis_detail = f"多重模运算异常分析: 监控设施余数={monitoring_facility_remainder:.1f}, 安全感设施余数={safety_facility_remainder:.1f}, 多重模数和={multiple_modular_sum:.1f}, 多重模数阈值={multiple_modular_threshold}, 多重模数超量={multiple_modular_excess:.1f}, 多重模数异常因子={multiple_modular_anomaly_factor:.2f}, 多重模数功能障碍度={multiple_modular_dysfunction:.1f}%"
        # 条件判断13: D4
        if z / 10 + w > m ** 2 + 80:
            type_code = 'D4'
            monitoring_safety_sum = z / 10 + w
            facility_squared_threshold = m ** 2 + 80
            analysis_detail = f"监控安全和设施超限分析: 监控安全和={monitoring_safety_sum:.2f}, 设施平方阈值={facility_squared_threshold:.1f}, 和超限度={min((monitoring_safety_sum - facility_squared_threshold) * 0.5, 95):.1f}%"

        # 条件判断14: D5
        if (z / 10 + w) / 2 < m * 10 + 40:
            type_code = 'D5'
            monitoring_safety_average = (z / 10 + w) / 2
            facility_multiple_threshold = m * 10 + 40
            analysis_detail = f"平均值收敛状态分析: 监控安全均值={(z / 10 + w) / 2:.2f}, 设施倍数阈值={facility_multiple_threshold:.1f}, 收敛优化度={min((facility_multiple_threshold - monitoring_safety_average) * 0.6, 95):.1f}%"

        # 条件判断15: D6
        if w ** 2 / 100 > z / 10 + m * 5:
            type_code = 'D6'
            safety_squared_scaled = w ** 2 / 100
            monitoring_facility_threshold = z / 10 + m * 5
            analysis_detail = f"安全平方设施超限分析: 安全平方缩放={safety_squared_scaled:.2f}, 监控设施阈值={monitoring_facility_threshold:.1f}, 平方超限度={min((safety_squared_scaled - monitoring_facility_threshold) * 0.4, 95):.1f}%"

        # 条件判断16: D7 (来自程序4.py, 原文件D6后缺少D7)
        # (程序4.py中D6是最后一个, 但TYPE_DEF中有D7, 我将添加一个占位符逻辑)
        if z / (w + 1) + m > 10:  # 这是一个示例逻辑, 因为原文件缺少D7的实现
            type_code = 'D7'
            analysis_detail = f"倒数和超限分析: 示例逻辑 {z / (w + 1) + m:.2f}, 阈值=10"

        # 发送分析结果回主进程 (Global Rank 12)
        result = {'code': type_code, 'detail': analysis_detail}
        comm.send(result, dest=12, tag=300)

    # -----------------------------------------------------------------
    # --- 程序5：物流配送分析 (Ranks 16-19) ---
    # -----------------------------------------------------------------
    elif rank == 16:
        # 进程16：主进程 (Global Rank 16)：负责数据生成、分发和宏观配送效率分析

        # 1. 随机生成五个核心物流配送变量
        x = random.randint(50, 500)  # 配送订单量 (50-500 单/小时)
        y = random.randint(40, 100)  # 配送效率 (40-100%)
        z = random.randint(30, 95)  # 路径优化率 (30-95%)
        w = random.randint(40, 100)  # 车辆利用率 (40-100%)
        m = random.randint(1, 10)  # 服务评分 (1-10分)

        # 存储数据
        logistics_data = [x, y, z, w, m]

        # 2. 分发数据到其他进程 (Ranks 17, 18, 19)
        # 发给进程 17：x, y, z (订单效率平衡分析)
        comm.send(x, dest=17, tag=1)
        comm.send(y, dest=17, tag=2)
        comm.send(z, dest=17, tag=3)

        # 发给进程 18：y, z, w (路径车辆协调分析)
        comm.send(y, dest=18, tag=1)
        comm.send(z, dest=18, tag=2)
        comm.send(w, dest=18, tag=3)

        # 发给进程 19：z, w, m (配送优化分析)
        comm.send(z, dest=19, tag=1)
        comm.send(w, dest=19, tag=2)
        comm.send(m, dest=19, tag=3)

        # 3. 执行宏观配送效率分析 (xyzwm)
        type_code = 'A0'  # 默认为配送效率平衡状态
        analysis_detail = ""

        # 条件判断1: if x > y * z / 10 + 200
        if x > y * z / 10 + 200:
            type_code = 'A1'
            order_volume = x
            efficiency_optimization_capacity = y * z / 10 + 200
            order_load_excess = order_volume - efficiency_optimization_capacity
            load_saturation_ratio = order_volume / efficiency_optimization_capacity if efficiency_optimization_capacity > 0 else float(
                'inf')
            order_overload_severity = min(load_saturation_ratio * 35, 100)
            analysis_detail = f"订单负载超限分析: 订单量={order_volume}单/h, 效率优化容量={efficiency_optimization_capacity:.1f}, 负载超量={order_load_excess:.1f}单/h, 负载饱和比={load_saturation_ratio:.2f}, 订单超载严重度={order_overload_severity:.1f}%"

        # 条件判断2: if w ** 2 + z < y * m * 15
        if w ** 2 + z < y * m * 15:
            type_code = 'A2'
            vehicle_utilization_squared = w ** 2
            path_optimization = z
            vehicle_path_aggregate = vehicle_utilization_squared + path_optimization
            efficiency_service_baseline = y * m * 15
            efficiency_match_deficit = efficiency_service_baseline - vehicle_path_aggregate
            efficiency_insufficiency_ratio = efficiency_match_deficit / vehicle_path_aggregate if vehicle_path_aggregate > 0 else float(
                'inf')
            efficiency_matching_inadequacy = min(efficiency_insufficiency_ratio * 32, 95)
            analysis_detail = f"效率匹配不足分析: 车辆利用平方={vehicle_utilization_squared}, 路径优化={path_optimization}%, 车辆路径聚合={vehicle_path_aggregate:.1f}, 效率服务基线={efficiency_service_baseline:.1f}, 效率匹配缺口={efficiency_match_deficit:.1f}, 效率不足比={efficiency_insufficiency_ratio:.2f}, 效率匹配不足度={efficiency_matching_inadequacy:.1f}%"

        # 条件判断3: if x + w * 2 > y + z * 3 + m * 10
        if x + w * 2 > y + z * 3 + m * 10:
            type_code = 'A3'
            order_vehicle_aggregate = x + w * 2
            efficiency_path_service_baseline = y + z * 3 + m * 10
            comprehensive_delivery_imbalance = order_vehicle_aggregate - efficiency_path_service_baseline
            delivery_coordination_strain = comprehensive_delivery_imbalance / efficiency_path_service_baseline if efficiency_path_service_baseline > 0 else float(
                'inf')
            comprehensive_delivery_stress = min(delivery_coordination_strain * 28, 95)
            analysis_detail = f"综合配送失衡分析: 订单车辆聚合={order_vehicle_aggregate:.1f}, 效率路径服务基线={efficiency_path_service_baseline:.1f}, 综合配送失衡量={comprehensive_delivery_imbalance:.1f}, 配送协调张力={delivery_coordination_strain:.2f}, 综合配送压力={comprehensive_delivery_stress:.1f}%"
        # 条件判断4: A4
        if x / 10 + y > z + w + m * 10:
            type_code = 'A4'
            order_efficiency_sum = x / 10 + y
            path_vehicle_service_threshold = z + w + m * 10
            analysis_detail = f"订单效率路径车辆和超限分析: 订单效率和={order_efficiency_sum:.2f}, 路径车辆服务阈值={path_vehicle_service_threshold:.1f}, 和超限度={min((order_efficiency_sum - path_vehicle_service_threshold) * 0.4, 95):.1f}%"

        # 条件判断5: A5
        if (x / 10 + y) ** 2 / 100 < z + w + m * 15:
            type_code = 'A5'
            order_efficiency_square_scaled = (x / 10 + y) ** 2 / 100
            path_vehicle_service_sum = z + w + m * 15
            analysis_detail = f"综合平方收敛状态分析: 订单效率平方缩放={(x / 10 + y) ** 2 / 100:.2f}, 路径车辆服务和={path_vehicle_service_sum:.1f}, 收敛优化度={min((path_vehicle_service_sum - order_efficiency_square_scaled) * 0.2, 95):.1f}%"

        # 条件判断6: A6
        if x / 10 + y > z * m + w * 2:
            type_code = 'A6'
            order_efficiency_sum = x / 10 + y
            path_service_vehicle_threshold = z * m + w * 2
            analysis_detail = f"订单效率和异常分析: 订单效率和={order_efficiency_sum:.2f}, 路径服务车辆阈值={path_service_vehicle_threshold:.1f}, 和异常度={min((order_efficiency_sum - path_service_vehicle_threshold) * 0.5, 95):.1f}%"

        # 4. 收集其他进程的分析结果 (Ranks 17, 18, 19)
        order_efficiency_result = comm.recv(source=17, tag=100, status=status)
        path_vehicle_result = comm.recv(source=18, tag=200, status=status)
        delivery_optimization_result = comm.recv(source=19, tag=300, status=status)

        # 5. 组装完整结果
        analysis_results = [
            f"宏观配送效率 (xyzwm): {type_code} -> {LOGISTICS_TYPE_DEF.get(type_code, '未知')} | {analysis_detail}",
            f"订单效率平衡 (xyz): {order_efficiency_result['code']} -> {LOGISTICS_TYPE_DEF.get(order_efficiency_result['code'], '未知')} | {order_efficiency_result['detail']}",
            f"路径车辆协调 (yzw): {path_vehicle_result['code']} -> {LOGISTICS_TYPE_DEF.get(path_vehicle_result['code'], '未知')} | {path_vehicle_result['detail']}",
            f"配送优化分析 (zwm): {delivery_optimization_result['code']} -> {LOGISTICS_TYPE_DEF.get(delivery_optimization_result['code'], '未知')} | {delivery_optimization_result['detail']}"
        ]

        # 6. 打印报告
        print("=" * 70)
        print(f"  物流配送分析系统 (进程 16-19)  ")
        print("=" * 70)
        print()
        print("--- 实时物流配送数据 ---")
        print(f"配送订单量(X): {x} 单/小时")
        print(f"配送效率(Y): {y}%")
        print(f"路径优化率(Z): {z}%")
        print(f"车辆利用率(W): {w}%")
        print(f"服务评分(M): {m} 分")
        print()
        print("--- 物流配送综合分析报告 ---")
        for i, result in enumerate(analysis_results, 1):
            print(f"{i}. {result}")
        print()
        print("=" * 70)
        print(f"程序5 (Ranks 16-19) 分析完成")
        print("=" * 70)
        print("\n")  # 增加间距

    elif rank == 17:
        # 进程17 (原 进程1)：接收 x, y, z 进行订单效率平衡分析
        x = comm.recv(source=16, tag=1, status=status)
        y = comm.recv(source=16, tag=2, status=status)
        z = comm.recv(source=16, tag=3, status=status)

        type_code = 'B0'  # 默认为订单效率平衡
        analysis_detail = ""

        # 条件判断4: if x ** 2 > y * z * 50 + 10000
        if x ** 2 > y * z * 50 + 10000:
            type_code = 'B1'
            order_volume_squared = x ** 2
            efficiency_path_product = y * z * 50 + 10000
            square_efficiency_excess = order_volume_squared - efficiency_path_product
            square_efficiency_amplification = order_volume_squared / efficiency_path_product if efficiency_path_product > 0 else float(
                'inf')
            square_efficiency_anomaly_level = min(square_efficiency_amplification * 25, 95)
            analysis_detail = f"平方效率异常分析: 订单量平方={order_volume_squared}, 效率路径乘积={efficiency_path_product:.1f}, 平方效率超量={square_efficiency_excess:.1f}, 平方效率放大度={square_efficiency_amplification:.2f}, 平方效率异常水平={square_efficiency_anomaly_level:.1f}%"

        # 条件判断5: if x % (y + z) > 30
        if x % (y + z) > 30:
            type_code = 'B2'
            order_volume = x
            efficiency_optimization_sum = y + z
            order_modular_remainder = x % efficiency_optimization_sum if efficiency_optimization_sum > 0 else 0
            fluctuation_threshold = 30
            order_fluctuation_excess = order_modular_remainder - fluctuation_threshold
            order_fluctuation_intensity = order_fluctuation_excess / fluctuation_threshold if fluctuation_threshold > 0 else 0
            order_fluctuation_risk = min(order_fluctuation_intensity * 38, 95)
            analysis_detail = f"订单波动超限分析: 订单量={order_volume}单/h, 效率优化和={efficiency_optimization_sum:.1f}, 订单模数余数={order_modular_remainder:.1f}, 波动阈值={fluctuation_threshold}, 订单波动超量={order_fluctuation_excess:.1f}, 订单波动强度={order_fluctuation_intensity:.2f}, 订单波动风险度={order_fluctuation_risk:.1f}%"

        # 条件判断6: if y + z < x / 4 + 80
        if y + z < x / 4 + 80:
            type_code = 'B3'
            delivery_efficiency = y
            path_optimization = z
            efficiency_path_sum = y + z
            order_quarter_baseline = x / 4 + 80
            efficiency_gap_magnitude = order_quarter_baseline - efficiency_path_sum
            efficiency_insufficiency_ratio = efficiency_gap_magnitude / efficiency_path_sum if efficiency_path_sum > 0 else 0
            efficiency_gap_severity = min(efficiency_insufficiency_ratio * 30, 95)
            analysis_detail = f"效率缺口过大分析: 配送效率={delivery_efficiency}%, 路径优化={path_optimization}%, 效率路径和={efficiency_path_sum:.1f}, 订单四分之一基线={order_quarter_baseline:.1f}, 效率缺口幅度={efficiency_gap_magnitude:.1f}, 效率不足比={efficiency_insufficiency_ratio:.2f}, 效率缺口严重度={efficiency_gap_severity:.1f}%"
        # 条件判断7: B4
        if x / 10 + y > z + 100:
            type_code = 'B4'
            order_efficiency_sum = x / 10 + y
            path_threshold = z + 100
            analysis_detail = f"订单效率和路径超限分析: 订单效率和={order_efficiency_sum:.2f}, 路径阈值={path_threshold:.1f}, 和超限度={min((order_efficiency_sum - path_threshold) * 0.3, 95):.1f}%"

        # 条件判断8: B5
        if (x / 10 + y) / 2 > z + 50:
            type_code = 'B5'
            order_efficiency_average = (x / 10 + y) / 2
            path_threshold = z + 50
            analysis_detail = f"平均值路径失衡分析: 订单效率均值={(x / 10 + y) / 2:.2f}, 路径阈值={path_threshold:.1f}, 平均失衡度={min((order_efficiency_average - path_threshold) * 0.6, 95):.1f}%"

        # 发送分析结果回主进程 (Global Rank 16)
        result = {'code': type_code, 'detail': analysis_detail}
        comm.send(result, dest=16, tag=100)


    elif rank == 18:
        # 进程18 (原 进程2)：接收 y, z, w 进行路径车辆协调分析
        y = comm.recv(source=16, tag=1, status=status)
        z = comm.recv(source=16, tag=2, status=status)
        w = comm.recv(source=16, tag=3, status=status)

        type_code = 'C0'  # 默认为路径车辆协调
        analysis_detail = ""

        # 条件判断7: if z ** 2 < w * y + 1500
        if z ** 2 < w * y + 1500:
            type_code = 'C1'
            path_optimization_squared = z ** 2
            vehicle_efficiency_product = w * y + 1500
            path_optimization_deficit = vehicle_efficiency_product - path_optimization_squared
            path_optimization_insufficiency = path_optimization_deficit / path_optimization_squared if path_optimization_squared > 0 else float(
                'inf')
            path_optimization_inadequacy = min(path_optimization_insufficiency * 33, 95)
            analysis_detail = f"路径优化不足分析: 路径优化平方={path_optimization_squared:.1f}, 车辆效率乘积={vehicle_efficiency_product:.1f}, 路径优化缺口={path_optimization_deficit:.1f}, 路径优化不足度={path_optimization_insufficiency:.2f}, 路径优化不足度={path_optimization_inadequacy:.1f}%"

        # 条件判断8: if (y * w) ** 2 > z ** 3 + 50000
        if (y * w) ** 2 > z ** 3 + 50000:
            type_code = 'C2'
            efficiency_vehicle_product = y * w
            efficiency_vehicle_squared = (y * w) ** 2
            path_cubic_capacity = z ** 3 + 50000
            vehicle_coordination_excess = efficiency_vehicle_squared - path_cubic_capacity
            vehicle_coordination_amplification = efficiency_vehicle_squared / path_cubic_capacity if path_cubic_capacity > 0 else float(
                'inf')
            vehicle_coordination_anomaly = min(vehicle_coordination_amplification * 22, 95)
            analysis_detail = f"车辆协调异常分析: 效率车辆乘积={efficiency_vehicle_product:.1f}, 效率车辆平方={efficiency_vehicle_squared:.1f}, 路径立方容量={path_cubic_capacity:.1f}, 车辆协调超量={vehicle_coordination_excess:.1f}, 车辆协调放大度={vehicle_coordination_amplification:.2f}, 车辆协调异常度={vehicle_coordination_anomaly:.1f}%"

        # 条件判断9: if y % (z // 5 + 1) == w % 8
        if y % (z // 5 + 1) == w % 8:
            type_code = 'C3'
            delivery_efficiency = y
            path_five_segment = z // 5 + 1
            efficiency_modular_remainder = y % path_five_segment if path_five_segment > 0 else 0
            vehicle_utilization = w
            vehicle_modular_remainder = w % 8
            modular_synchronization_indicator = 1 if efficiency_modular_remainder == vehicle_modular_remainder else 0
            cyclical_synchronization_anomaly = modular_synchronization_indicator * 88 + abs(
                efficiency_modular_remainder - vehicle_modular_remainder) * 3
            analysis_detail = f"周期同步失调分析: 配送效率={delivery_efficiency}%, 路径五分段={path_five_segment}, 效率模数余数={efficiency_modular_remainder:.1f}, 车辆利用率={vehicle_utilization}%, 车辆模数余数={vehicle_modular_remainder:.1f}, 模运算同步指示={modular_synchronization_indicator}, 周期同步异常度={cyclical_synchronization_anomaly:.1f}%"
        # 条件判断10: C4
        if y + w > z + 100:
            type_code = 'C4'
            efficiency_vehicle_sum = y + w
            path_threshold = z + 100
            analysis_detail = f"效率车辆和路径超限分析: 效率车辆和={efficiency_vehicle_sum:.1f}, 路径阈值={path_threshold:.1f}, 和超限度={min((efficiency_vehicle_sum - path_threshold) * 0.5, 95):.1f}%"

        # 条件判断11: C5
        if (y + w) ** 2 / 100 < z * 8 + 50:
            type_code = 'C5'
            efficiency_vehicle_square_scaled = (y + w) ** 2 / 100
            path_multiple_threshold = z * 8 + 50
            analysis_detail = f"平方和收敛状态分析: 效率车辆平方缩放={(y + w) ** 2 / 100:.2f}, 路径倍数阈值={path_multiple_threshold:.1f}, 收敛优化度={min((path_multiple_threshold - efficiency_vehicle_square_scaled) * 0.15, 95):.1f}%"

        # 条件判断12: C6
        if w / (z + 1) + y / 10 > 5:
            type_code = 'C6'
            vehicle_path_efficiency_sum = w / (z + 1) + y / 10
            reciprocal_threshold = 5
            analysis_detail = f"倒数和超限分析: 车辆路径效率和={vehicle_path_efficiency_sum:.2f}, 倒数阈值={reciprocal_threshold:.1f}, 倒数和超限度={min((vehicle_path_efficiency_sum - reciprocal_threshold) * 8, 95):.1f}%"

        # 发送分析结果回主进程 (Global Rank 16)
        result = {'code': type_code, 'detail': analysis_detail}
        comm.send(result, dest=16, tag=200)


    elif rank == 19:
        # 进程19 (原 进程3)：接收 z, w, m 进行配送优化分析
        z = comm.recv(source=16, tag=1, status=status)
        w = comm.recv(source=16, tag=2, status=status)
        m = comm.recv(source=16, tag=3, status=status)

        type_code = 'D0'  # 默认为配送优化平衡
        analysis_detail = ""

        # 条件判断10: if z ** 3 > w ** 2 * m * 800
        if z ** 3 > w ** 2 * m * 800:
            type_code = 'D1'
            path_optimization_cubed = z ** 3
            vehicle_service_squared_product = w ** 2 * m * 800
            cubic_load_excess = path_optimization_cubed - vehicle_service_squared_product
            cubic_load_amplification = path_optimization_cubed / vehicle_service_squared_product if vehicle_service_squared_product > 0 else float(
                'inf')
            cubic_load_saturation = min(cubic_load_amplification * 24, 95)
            analysis_detail = f"立方负载超限分析: 路径优化立方={path_optimization_cubed:.1f}, 车辆服务平方乘积={vehicle_service_squared_product:.1f}, 立方负载超量={cubic_load_excess:.1f}, 立方负载放大度={cubic_load_amplification:.2f}, 立方负载饱和度={cubic_load_saturation:.1f}%"

        # 条件判断11: if (z + w) / (m + 3) > 30
        if (z + w) / (m + 3) > 30:
            type_code = 'D2'
            path_vehicle_sum = z + w
            service_adjusted_divisor = m + 3
            service_quality_ratio = path_vehicle_sum / service_adjusted_divisor
            service_quality_threshold = 30
            service_quality_excess = service_quality_ratio - service_quality_threshold
            service_quality_anomaly_factor = service_quality_excess / service_quality_threshold if service_quality_threshold > 0 else 0
            service_quality_dysfunction = min(service_quality_anomaly_factor * 31, 95)
            analysis_detail = f"服务质量异常分析: 路径车辆和={path_vehicle_sum:.1f}, 服务调整除数={service_adjusted_divisor:.1f}, 服务质量比={service_quality_ratio:.2f}, 服务质量阈值={service_quality_threshold}, 服务质量超量={service_quality_excess:.2f}, 服务质量异常因子={service_quality_anomaly_factor:.2f}, 服务质量功能障碍度={service_quality_dysfunction:.1f}%"

        # 条件判断12: if z * w + m ** 2 * 10 > 8500
        if z * w + m ** 2 * 10 > 8500:
            type_code = 'D3'
            path_vehicle_product = z * w
            service_squared_component = m ** 2 * 10
            comprehensive_optimization_aggregate = path_vehicle_product + service_squared_component
            comprehensive_optimization_threshold = 8500
            comprehensive_optimization_overload = comprehensive_optimization_aggregate - comprehensive_optimization_threshold
            comprehensive_overload_ratio = comprehensive_optimization_overload / comprehensive_optimization_threshold if comprehensive_optimization_threshold > 0 else 0
            comprehensive_optimization_saturation = min(comprehensive_overload_ratio * 27, 95)
            analysis_detail = f"综合优化超载分析: 路径车辆乘积={path_vehicle_product:.1f}, 服务平方分量={service_squared_component:.1f}, 综合优化聚合={comprehensive_optimization_aggregate:.1f}, 综合优化阈值={comprehensive_optimization_threshold}, 综合优化过载量={comprehensive_optimization_overload:.1f}, 综合过载比={comprehensive_overload_ratio:.2f}, 综合优化饱和度={comprehensive_optimization_saturation:.1f}%"
        # 条件判断13: D4
        if z + w > m ** 2 + 100:
            type_code = 'D4'
            path_vehicle_sum = z + w
            service_squared_threshold = m ** 2 + 100
            analysis_detail = f"路径车辆和服务超限分析: 路径车辆和={path_vehicle_sum:.1f}, 服务平方阈值={service_squared_threshold:.1f}, 和超限度={min((path_vehicle_sum - service_squared_threshold) * 0.4, 95):.1f}%"

        # 条件判断14: D5
        if (z + w) / 2 < m * 15 + 50:
            type_code = 'D5'
            path_vehicle_average = (z + w) / 2
            service_multiple_threshold = m * 15 + 50
            analysis_detail = f"平均值收敛状态分析: 路径车辆均值={(z + w) / 2:.2f}, 服务倍数阈值={service_multiple_threshold:.1f}, 收敛优化度={min((service_multiple_threshold - path_vehicle_average) * 0.6, 95):.1f}%"

        # 条件判断15: D6
        if w ** 2 / 10 > z * m + 80:
            type_code = 'D6'
            vehicle_squared_scaled = w ** 2 / 10
            path_service_product_threshold = z * m + 80
            analysis_detail = f"车辆平方服务超限分析: 车辆平方缩放={vehicle_squared_scaled:.2f}, 路径服务积阈值={path_service_product_threshold:.1f}, 平方超限度={min((vehicle_squared_scaled - path_service_product_threshold) * 0.3, 95):.1f}%"

        # 条件判断16: D7
        if z / (m + 1) + w / (m + 2) > 50:
            type_code = 'D7'
            path_vehicle_reciprocal_sum = z / (m + 1) + w / (m + 2)
            reciprocal_threshold = 50
            analysis_detail = f"倒数和超限分析: 路径车辆倒数和={path_vehicle_reciprocal_sum:.2f}, 倒数阈值={reciprocal_threshold:.1f}, 倒数和超限度={min((path_vehicle_reciprocal_sum - reciprocal_threshold) * 1, 95):.1f}%"

        # 发送分析结果回主进程 (Global Rank 16)
        result = {'code': type_code, 'detail': analysis_detail}
        comm.send(result, dest=16, tag=300)

    # -----------------------------------------------------------------
    # --- 程序6：人口流动监控分析 (Ranks 20-23) ---
    # -----------------------------------------------------------------
    elif rank == 20:
        # 进程20：主进程 (Global Rank 20)：负责数据生成、分发和宏观人口流动分析

        # 1. 随机生成五个核心人口流动变量
        x = random.randint(100, 5000)  # 人员流动速度 (100-5000 人/小时)
        y = random.randint(500, 20000)  # 区域人口密度 (500-20000 人/平方公里)
        z = random.randint(20, 90)  # 居住分布均匀度 (20-90%)
        w = random.randint(40, 100)  # 年龄结构多样性 (40-100%)
        m = random.randint(1, 10)  # 社区设施完备度 (1-10分)

        # 存储数据
        population_data = [x, y, z, w, m]

        # 2. 分发数据到其他进程 (Ranks 21, 22, 23)
        # 发给进程 21：x, y, z (流动密度平衡分析)
        comm.send(x, dest=21, tag=1)
        comm.send(y, dest=21, tag=2)
        comm.send(z, dest=21, tag=3)

        # 发给进程 22：y, z, w (分布多样性协调分析)
        comm.send(y, dest=22, tag=1)
        comm.send(z, dest=22, tag=2)
        comm.send(w, dest=22, tag=3)

        # 发给进程 23：z, w, m (人口优化分析)
        comm.send(z, dest=23, tag=1)
        comm.send(w, dest=23, tag=2)
        comm.send(m, dest=23, tag=3)

        # 3. 执行宏观人口流动分析 (xyzwm)
        type_code = 'A0'  # 默认为人口流动平衡状态
        analysis_detail = ""

        # 条件判断1: if (x - y / 4) ** 2 + z > w * m + 200
        if (x - y / 4) ** 2 + z > w * m + 200:
            type_code = 'A1'
            flow_density_difference = x - y / 4
            flow_density_square_deviation = flow_density_difference ** 2
            distribution_uniformity = z
            square_deviation_aggregate = flow_density_square_deviation + distribution_uniformity
            age_facility_baseline = w * m + 200
            square_deviation_excess = square_deviation_aggregate - age_facility_baseline
            flow_density_square_anomaly = square_deviation_excess / age_facility_baseline if age_facility_baseline > 0 else 0
            flow_density_square_dysfunction = min(flow_density_square_anomaly * 27, 95)
            analysis_detail = f"流动密度平方差异常分析: 流动密度差值={flow_density_difference:.1f}, 流动密度平方偏差={flow_density_square_deviation:.1f}, 分布均匀度={distribution_uniformity}%, 平方偏差聚合={square_deviation_aggregate:.1f}, 年龄设施基线={age_facility_baseline:.1f}, 平方偏差超量={square_deviation_excess:.1f}, 流动密度平方异常度={flow_density_square_anomaly:.2f}, 流动密度平方功能障碍度={flow_density_square_dysfunction:.1f}%"

        # 条件判断2: if x ** (1/3) + y ** 0.4 < z + w + m * 15
        if x ** (1 / 3) + y ** 0.4 < z + w + m * 15:
            type_code = 'A2'
            flow_cube_root = x ** (1 / 3)
            density_fractional_power = y ** 0.4
            fractional_power_combination = flow_cube_root + density_fractional_power
            distribution_age_facility_sum = z + w + m * 15
            fractional_power_deficit = distribution_age_facility_sum - fractional_power_combination
            fractional_power_insufficiency = fractional_power_deficit / fractional_power_combination if fractional_power_combination > 0 else 0
            fractional_power_inadequacy = min(fractional_power_insufficiency * 33, 95)
            analysis_detail = f"分数幂组合不足分析: 流动立方根={flow_cube_root:.2f}, 密度分数幂={density_fractional_power:.2f}, 分数幂组合值={fractional_power_combination:.2f}, 分布年龄设施和={distribution_age_facility_sum:.1f}, 分数幂缺口={fractional_power_deficit:.2f}, 分数幂不足度={fractional_power_insufficiency:.2f}, 分数幂不足度={fractional_power_inadequacy:.1f}%"

        # 条件判断3: if x * y / 1000 > z ** 2 + w ** 2 + m ** 3
        if x * y / 1000 > z ** 2 + w ** 2 + m ** 3:
            type_code = 'A3'
            flow_density_thousand_product = x * y / 1000
            distribution_squared = z ** 2
            age_squared = w ** 2
            facility_cubed = m ** 3
            multi_power_combination = distribution_squared + age_squared + facility_cubed
            multi_power_excess = flow_density_thousand_product - multi_power_combination
            multi_power_overload_ratio = multi_power_excess / multi_power_combination if multi_power_combination > 0 else 0
            multi_power_saturation = min(multi_power_overload_ratio * 24, 95)
            analysis_detail = f"多次幂组合超载分析: 流动密度千分积={flow_density_thousand_product:.1f}, 分布平方={distribution_squared:.1f}, 年龄平方={age_squared:.1f}, 设施立方={facility_cubed:.1f}, 多次幂组合值={multi_power_combination:.1f}, 多次幂超量={multi_power_excess:.1f}, 多次幂过载比={multi_power_overload_ratio:.2f}, 多次幂饱和度={multi_power_saturation:.1f}%"
        # 条件判断4: A4
        if (x / 100 - y / 1000) ** 2 * 10 > m ** 3 + z * w / 10:
            type_code = 'A4'
            gradient_square_amplified = (x / 100 - y / 1000) ** 2 * 10
            facility_cubic_baseline = m ** 3 + z * w / 10
            analysis_detail = f"流动密度梯度与设施幂次对比分析: 梯度平方放大={gradient_square_amplified:.2f}, 设施立方基线={facility_cubic_baseline:.2f}, 梯度对比异常度={min((gradient_square_amplified - facility_cubic_baseline) / facility_cubic_baseline * 25, 95) if facility_cubic_baseline > 0 else 0:.1f}%"

        # 条件判断5: A5
        if ((x + y / 10) ** 0.5) ** 0.5 + z ** 0.5 < w ** 0.5 + m * 3:
            type_code = 'A5'
            nested_root_sum = ((x + y / 10) ** 0.5) ** 0.5 + z ** 0.5
            age_facility_baseline = w ** 0.5 + m * 3
            analysis_detail = f"多重开方嵌套组合分析: 嵌套开方和={nested_root_sum:.2f}, 年龄设施基线={age_facility_baseline:.2f}, 嵌套组合不足度={min((age_facility_baseline - nested_root_sum) / nested_root_sum * 32, 95) if nested_root_sum > 0 else 0:.1f}%"

        # 4. 收集其他进程的分析结果 (Ranks 21, 22, 23)
        flow_density_result = comm.recv(source=21, tag=100, status=status)
        distribution_diversity_result = comm.recv(source=22, tag=200, status=status)
        population_optimization_result = comm.recv(source=23, tag=300, status=status)

        # 5. 组装完整结果
        analysis_results = [
            f"宏观人口流动 (xyzwm): {type_code} -> {POPULATION_TYPE_DEF.get(type_code, '未知')} | {analysis_detail}",
            f"流动密度平衡 (xyz): {flow_density_result['code']} -> {POPULATION_TYPE_DEF.get(flow_density_result['code'], '未知')} | {flow_density_result['detail']}",
            f"分布多样性协调 (yzw): {distribution_diversity_result['code']} -> {POPULATION_TYPE_DEF.get(distribution_diversity_result['code'], '未知')} | {distribution_diversity_result['detail']}",
            f"人口优化分析 (zwm): {population_optimization_result['code']} -> {POPULATION_TYPE_DEF.get(population_optimization_result['code'], '未知')} | {population_optimization_result['detail']}"
        ]

        # 6. 打印报告
        print("=" * 70)
        print(f"  人口流动监控系统 (进程 20-23)  ")
        print("=" * 70)
        print()
        print("--- 实时人口流动数据 ---")
        print(f"人员流动速度(X): {x} 人/小时")
        print(f"区域人口密度(Y): {y} 人/平方公里")
        print(f"居住分布均匀度(Z): {z}%")
        print(f"年龄结构多样性(W): {w}%")
        print(f"社区设施完备度(M): {m} 分")
        print()
        print("--- 人口流动综合分析报告 ---")
        for i, result in enumerate(analysis_results, 1):
            print(f"{i}. {result}")
        print()
        print("=" * 70)
        print(f"程序6 (Ranks 20-23) 分析完成")
        print("=" * 70)
        print("\n")  # 增加间距

    elif rank == 21:
        # 进程21 (原 进程1)：接收 x, y, z 进行流动密度平衡分析
        x = comm.recv(source=20, tag=1, status=status)
        y = comm.recv(source=20, tag=2, status=status)
        z = comm.recv(source=20, tag=3, status=status)

        type_code = 'B0'  # 默认为流动密度平衡
        analysis_detail = ""

        # 条件判断4: if x ** 2 - y * 10 + z ** 2 > 15000
        if x ** 2 - y * 10 + z ** 2 > 15000:
            type_code = 'B1'
            flow_speed_squared = x ** 2
            density_ten_multiple = y * 10
            distribution_squared = z ** 2
            quadratic_equation_result = flow_speed_squared - density_ten_multiple + distribution_squared
            quadratic_threshold = 15000
            quadratic_excess = quadratic_equation_result - quadratic_threshold
            quadratic_imbalance_factor = quadratic_excess / quadratic_threshold if quadratic_threshold > 0 else 0
            quadratic_equation_dysfunction = min(quadratic_imbalance_factor * 29, 95)
            analysis_detail = f"二次方程失衡分析: 流动速度平方={flow_speed_squared}, 密度10倍={density_ten_multiple:.1f}, 分布平方={distribution_squared:.1f}, 二次方程结果={quadratic_equation_result:.1f}, 二次方程阈值={quadratic_threshold}, 二次方程超量={quadratic_excess:.1f}, 二次失衡因子={quadratic_imbalance_factor:.2f}, 二次方程功能障碍度={quadratic_equation_dysfunction:.1f}%"

        # 条件判断5: if x / (y + z) + y / (x + z) > 3
        if x / (y + z) + y / (x + z) > 3:
            type_code = 'B2'
            flow_to_density_distribution_ratio = x / (y + z) if (y + z) > 0 else 0
            density_to_flow_distribution_ratio = y / (x + z) if (x + z) > 0 else 0
            cross_ratio_sum = flow_to_density_distribution_ratio + density_to_flow_distribution_ratio
            cross_ratio_threshold = 3
            cross_ratio_excess = cross_ratio_sum - cross_ratio_threshold
            cross_ratio_anomaly_factor = cross_ratio_excess / cross_ratio_threshold if cross_ratio_threshold > 0 else 0
            cross_ratio_dysfunction = min(cross_ratio_anomaly_factor * 32, 95)
            analysis_detail = f"交叉比值异常分析: 流动对密度分布比={flow_to_density_distribution_ratio:.2f}, 密度对流动分布比={density_to_flow_distribution_ratio:.2f}, 交叉比值和={cross_ratio_sum:.2f}, 交叉比值阈值={cross_ratio_threshold}, 交叉比值超量={cross_ratio_excess:.2f}, 交叉比值异常因子={cross_ratio_anomaly_factor:.2f}, 交叉比值功能障碍度={cross_ratio_dysfunction:.1f}%"

        # 条件判断6: if (x + y) ** 0.6 > z * 25 + 800
        if (x + y) ** 0.6 > z * 25 + 800:
            type_code = 'B3'
            flow_density_sum = x + y
            flow_density_fractional_power = (x + y) ** 0.6
            distribution_multiple_baseline = z * 25 + 800
            fractional_power_threshold_excess = flow_density_fractional_power - distribution_multiple_baseline
            fractional_power_threshold_ratio = fractional_power_threshold_excess / distribution_multiple_baseline if distribution_multiple_baseline > 0 else 0
            fractional_power_threshold_exceedance = min(fractional_power_threshold_ratio * 26, 95)
            analysis_detail = f"分数幂阈值超限分析: 流动密度和={flow_density_sum:.1f}, 流动密度分数幂={flow_density_fractional_power:.2f}, 分布倍数基线={distribution_multiple_baseline:.1f}, 分数幂阈值超量={fractional_power_threshold_excess:.2f}, 分数幂阈值比={fractional_power_threshold_ratio:.2f}, 分数幂阈值超限度={fractional_power_threshold_exceedance:.1f}%"
        # 条件判断7: B4
        if x ** 2 / 100 > (y / 100) ** 1.5 + z * 10:
            type_code = 'B4'
            flow_squared_scaled = x ** 2 / 100
            density_distribution_baseline = (y / 100) ** 1.5 + z * 10
            analysis_detail = f"流动速度与密度的对数级关系异常分析: 流动平方缩放={flow_squared_scaled:.2f}, 密度分布基线={density_distribution_baseline:.2f}, 对数级关系异常度={min((flow_squared_scaled - density_distribution_baseline) / density_distribution_baseline * 24, 95) if density_distribution_baseline > 0 else 0:.1f}%"

        # 条件判断8: B5
        if ((x + y / 20) ** 0.5 + z) ** 0.5 < 25:
            type_code = 'B5'
            nested_composite_root = ((x + y / 20) ** 0.5 + z) ** 0.5
            nested_threshold = 25
            analysis_detail = f"嵌套平方根与分布的复合关系分析: 嵌套复合开方={nested_composite_root:.2f}, 嵌套阈值={nested_threshold}, 嵌套复合不足度={min((nested_threshold - nested_composite_root) / nested_composite_root * 38, 95) if nested_composite_root > 0 else 0:.1f}%"

        # 条件判断9: B6
        if z * (x / (y / 100 + 1)) ** 0.5 > 800:
            type_code = 'B6'
            distribution_driven_regulation = z * (x / (y / 100 + 1)) ** 0.5
            regulation_threshold = 800
            analysis_detail = f"分布驱动的流动密度非线性调节分析: 分布驱动调节值={distribution_driven_regulation:.2f}, 调节阈值={regulation_threshold}, 非线性调节超载度={min((distribution_driven_regulation - regulation_threshold) / regulation_threshold * 21, 95):.1f}%"

        # 条件判断10: B7
        if (x * y / 10000) ** 0.4 + (x + y) ** 0.3 > z + 100:
            type_code = 'B7'
            segmented_power_combination = (x * y / 10000) ** 0.4 + (x + y) ** 0.3
            distribution_baseline = z + 100
            analysis_detail = f"流动密度交互的分段幂次分析: 分段幂次组合={segmented_power_combination:.2f}, 分布基线={distribution_baseline:.1f}, 分段幂次超载度={min((segmented_power_combination - distribution_baseline) / distribution_baseline * 27, 95) if distribution_baseline > 0 else 0:.1f}%"

        # 发送分析结果回主进程 (Global Rank 20)
        result = {'code': type_code, 'detail': analysis_detail}
        comm.send(result, dest=20, tag=100)

    elif rank == 22:
        # 进程22 (原 进程2)：接收 y, z, w 进行分布多样性协调分析
        y = comm.recv(source=20, tag=1, status=status)
        z = comm.recv(source=20, tag=2, status=status)
        w = comm.recv(source=20, tag=3, status=status)

        type_code = 'C0'  # 默认为分布多样性协调
        analysis_detail = ""

        # 条件判断7: if y ** 0.3 * w ** 0.7 < z * 30
        if y ** 0.3 * w ** 0.7 < z * 30:
            type_code = 'C1'
            density_fractional_power = y ** 0.3
            age_diversity_fractional_power = w ** 0.7
            fractional_power_product = density_fractional_power * age_diversity_fractional_power
            distribution_thirty_multiple = z * 30
            fractional_power_deficit = distribution_thirty_multiple - fractional_power_product
            fractional_power_insufficiency_ratio = fractional_power_deficit / fractional_power_product if fractional_power_product > 0 else 0
            fractional_power_product_inadequacy = min(fractional_power_insufficiency_ratio * 31, 95)
            analysis_detail = f"分数幂乘积不足分析: 密度分数幂={density_fractional_power:.2f}, 年龄多样性分数幂={age_diversity_fractional_power:.2f}, 分数幂乘积={fractional_power_product:.2f}, 分布30倍={distribution_thirty_multiple:.1f}, 分数幂乘积缺口={fractional_power_deficit:.2f}, 分数幂乘积不足比={fractional_power_insufficiency_ratio:.2f}, 分数幂乘积不足度={fractional_power_product_inadequacy:.1f}%"

        # 条件判断8: if (y - w * 50) ** 2 / 10000 > z / 3
        if (y - w * 50) ** 2 / 10000 > z / 3:
            type_code = 'C2'
            density_age_difference = y - w * 50
            density_age_square_difference = density_age_difference ** 2
            square_proportion_ratio = density_age_square_difference / 10000
            distribution_third = z / 3
            square_proportion_excess = square_proportion_ratio - distribution_third
            square_proportion_anomaly_factor = square_proportion_excess / distribution_third if distribution_third > 0 else 0
            square_proportion_dysfunction = min(square_proportion_anomaly_factor * 28, 95)
            analysis_detail = f"平方比例异常分析: 密度年龄差值={density_age_difference:.1f}, 密度年龄平方差={density_age_square_difference:.1f}, 平方比例比={square_proportion_ratio:.4f}, 分布三分之一={distribution_third:.2f}, 平方比例超量={square_proportion_excess:.4f}, 平方比例异常因子={square_proportion_anomaly_factor:.2f}, 平方比例功能障碍度={square_proportion_dysfunction:.1f}%"

        # 条件判断9: if y / 100 + w / 10 + z / 5 < 80
        if y / 100 + w / 10 + z / 5 < 80:
            type_code = 'C3'
            density_hundredth = y / 100
            age_tenth = w / 10
            distribution_fifth = z / 5
            fractional_weighted_sum = density_hundredth + age_tenth + distribution_fifth
            fractional_weighted_threshold = 80
            fractional_weighted_deficit = fractional_weighted_threshold - fractional_weighted_sum
            fractional_weighted_insufficiency = fractional_weighted_deficit / fractional_weighted_sum if fractional_weighted_sum > 0 else 0
            fractional_weighted_inadequacy = min(fractional_weighted_insufficiency * 35, 95)
            analysis_detail = f"分数加权和不足分析: 密度百分之一={density_hundredth:.2f}, 年龄十分之一={age_tenth:.1f}, 分布五分之一={distribution_fifth:.1f}, 分数加权和={fractional_weighted_sum:.2f}, 分数加权阈值={fractional_weighted_threshold}, 分数加权缺口={fractional_weighted_deficit:.2f}, 分数加权不足度={fractional_weighted_insufficiency:.2f}, 分数加权不足度={fractional_weighted_inadequacy:.1f}%"
        # 条件判断10: C4
        if (y * w) ** 0.5 / 10 < z ** 1.5 - 50:
            type_code = 'C4'
            geometric_mean_scaled = (y * w) ** 0.5 / 10
            distribution_adjusted_baseline = z ** 1.5 - 50
            analysis_detail = f"密度年龄几何平均与分布的幂次对比分析: 几何平均缩放={geometric_mean_scaled:.2f}, 分布调整基线={distribution_adjusted_baseline:.2f}, 几何平均不足度={min((distribution_adjusted_baseline - geometric_mean_scaled) / geometric_mean_scaled * 30, 95) if geometric_mean_scaled > 0 else 0:.1f}%"

        # 条件判断11: C5
        if z ** 2 / 100 + (y / 1000) * (w / 10) > 80:
            type_code = 'C5'
            polynomial_combination = z ** 2 / 100 + (y / 1000) * (w / 10)
            polynomial_threshold = 80
            analysis_detail = f"分布驱动的密度年龄多项式组合分析: 多项式组合值={polynomial_combination:.2f}, 多项式阈值={polynomial_threshold}, 多项式超载度={min((polynomial_combination - polynomial_threshold) / polynomial_threshold * 26, 95):.1f}%"

        # 条件判断12: C6
        if ((y / 100 - w) ** 2) ** 0.5 + z / 2 > 100:
            type_code = 'C6'
            nonlinear_transformation = ((y / 100 - w) ** 2) ** 0.5 + z / 2
            transformation_threshold = 100
            analysis_detail = f"密度年龄差值的非线性转换异常分析: 非线性转换值={nonlinear_transformation:.2f}, 转换阈值={transformation_threshold}, 非线性转换异常度={min((nonlinear_transformation - transformation_threshold) / transformation_threshold * 29, 95):.1f}%"

        # 条件判断13: C7
        if y ** 0.25 + z ** 0.6 + w ** 0.8 < 50:
            type_code = 'C7'
            multi_fractional_power_sum = y ** 0.25 + z ** 0.6 + w ** 0.8
            fractional_power_threshold = 50
            analysis_detail = f"多重分数幂加权协调失衡分析: 多重分数幂和={multi_fractional_power_sum:.2f}, 分数幂阈值={fractional_power_threshold}, 多重分数幂失衡度={min((fractional_power_threshold - multi_fractional_power_sum) / multi_fractional_power_sum * 33, 95) if multi_fractional_power_sum > 0 else 0:.1f}%"

        # 发送分析结果回主进程 (Global Rank 20)
        result = {'code': type_code, 'detail': analysis_detail}
        comm.send(result, dest=20, tag=200)

    elif rank == 23:
        # 进程23 (原 进程3)：接收 z, w, m 进行人口优化分析
        z = comm.recv(source=20, tag=1, status=status)
        w = comm.recv(source=20, tag=2, status=status)
        m = comm.recv(source=20, tag=3, status=status)

        type_code = 'D0'  # 默认为人口优化平衡
        analysis_detail = ""

        # 条件判断10: if z ** 3 + w ** 3 > m ** 2 * 5000
        if z ** 3 + w ** 3 > m ** 2 * 5000:
            type_code = 'D1'
            distribution_cubed = z ** 3
            age_diversity_cubed = w ** 3
            cubic_sum = distribution_cubed + age_diversity_cubed
            facility_squared_multiple = m ** 2 * 5000
            cubic_sum_excess = cubic_sum - facility_squared_multiple
            cubic_sum_overload_ratio = cubic_sum_excess / facility_squared_multiple if facility_squared_multiple > 0 else 0
            cubic_sum_saturation = min(cubic_sum_overload_ratio * 23, 95)
            analysis_detail = f"立方和超载分析: 分布立方={distribution_cubed:.1f}, 年龄多样性立方={age_diversity_cubed:.1f}, 立方和={cubic_sum:.1f}, 设施平方倍数={facility_squared_multiple:.1f}, 立方和超量={cubic_sum_excess:.1f}, 立方和过载比={cubic_sum_overload_ratio:.2f}, 立方和饱和度={cubic_sum_saturation:.1f}%"

        # 条件判断11: if (z * w) ** 0.5 + m ** 2 > 120
        if (z * w) ** 0.5 + m ** 2 > 120:
            type_code = 'D2'
            distribution_age_product = z * w
            distribution_age_square_root = (z * w) ** 0.5
            facility_squared = m ** 2
            square_root_square_combination = distribution_age_square_root + facility_squared
            square_root_square_threshold = 120
            square_root_square_excess = square_root_square_combination - square_root_square_threshold
            square_root_square_anomaly_ratio = square_root_square_excess / square_root_square_threshold if square_root_square_threshold > 0 else 0
            square_root_square_dysfunction = min(square_root_square_anomaly_ratio * 30, 95)
            analysis_detail = f"开方平方组合异常分析: 分布年龄乘积={distribution_age_product:.1f}, 分布年龄开方={distribution_age_square_root:.2f}, 设施平方={facility_squared:.1f}, 开方平方组合={square_root_square_combination:.2f}, 开方平方阈值={square_root_square_threshold}, 开方平方超量={square_root_square_excess:.2f}, 开方平方异常比={square_root_square_anomaly_ratio:.2f}, 开方平方功能障碍度={square_root_square_dysfunction:.1f}%"

        # 条件判断12: if z + w * m / 20 > (z + w) / 2 + 50
        if z + w * m / 20 > (z + w) / 2 + 50:
            type_code = 'D3'
            distribution_uniformity = z
            age_facility_weighted = w * m / 20
            weighted_combination = distribution_uniformity + age_facility_weighted
            distribution_age_average = (z + w) / 2
            average_baseline = distribution_age_average + 50
            weighted_average_excess = weighted_combination - average_baseline
            weighted_average_comparison_ratio = weighted_average_excess / average_baseline if average_baseline > 0 else 0
            weighted_average_comparison_anomaly = min(weighted_average_comparison_ratio * 27, 95)
            analysis_detail = f"加权平均对比异常分析: 分布均匀度={distribution_uniformity}%, 年龄设施加权={age_facility_weighted:.2f}, 加权组合值={weighted_combination:.2f}, 分布年龄平均={distribution_age_average:.1f}, 平均基线={average_baseline:.1f}, 加权平均超量={weighted_average_excess:.2f}, 加权平均对比比={weighted_average_comparison_ratio:.2f}, 加权平均对比异常度={weighted_average_comparison_anomaly:.1f}%"
        # 条件判断13: D4
        if (z * w) / ((z + w) / 2 + 1) > m ** 2 + 50:
            type_code = 'D4'
            logarithmic_transform = (z * w) / ((z + w) / 2 + 1)
            facility_squared_baseline = m ** 2 + 50
            analysis_detail = f"分布年龄乘积的对数变换与设施关系分析: 对数变换值={logarithmic_transform:.2f}, 设施平方基线={facility_squared_baseline:.1f}, 对数变换超载度={min((logarithmic_transform - facility_squared_baseline) / facility_squared_baseline * 25, 95) if facility_squared_baseline > 0 else 0:.1f}%"

        # 条件判断14: D5
        if 3 / (1 / z + 1 / w + 1 / (m * 10)) < 20:
            type_code = 'D5'
            harmonic_mean = 3 / (1 / z + 1 / w + 1 / (m * 10)) if (z > 0 and w > 0 and m > 0) else 0
            harmonic_threshold = 20
            analysis_detail = f"三变量调和平均与幂次组合分析: 调和平均={harmonic_mean:.2f}, 调和阈值={harmonic_threshold}, 调和平均不足度={min((harmonic_threshold - harmonic_mean) / harmonic_mean * 36, 95) if harmonic_mean > 0 else 0:.1f}%"

        # 条件判断15: D6
        if (w ** 0.5) * (m ** 1.5) > z * 15 + 300:
            type_code = 'D6'
            nonlinear_interaction = (w ** 0.5) * (m ** 1.5)
            distribution_linear_baseline = z * 15 + 300
            analysis_detail = f"年龄设施非线性交互与分布对比分析: 非线性交互值={nonlinear_interaction:.2f}, 分布线性基线={distribution_linear_baseline:.1f}, 非线性交互超载度={min((nonlinear_interaction - distribution_linear_baseline) / distribution_linear_baseline * 24, 95) if distribution_linear_baseline > 0 else 0:.1f}%"

        # 条件判断16: D7
        if ((z - w) ** 2) ** 0.5 / (m + 1) > 8:
            type_code = 'D7'
            square_root_ratio = ((z - w) ** 2) ** 0.5 / (m + 1)
            ratio_threshold = 8
            analysis_detail = f"分布年龄差值的平方根比值异常分析: 平方根比值={square_root_ratio:.2f}, 比值阈值={ratio_threshold}, 平方根比值异常度={min((square_root_ratio - ratio_threshold) / ratio_threshold * 31, 95):.1f}%"

        # 发送分析结果回主进程 (Global Rank 20)
        result = {'code': type_code, 'detail': analysis_detail}
        comm.send(result, dest=20, tag=300)


if __name__ == "__main__":
    main()