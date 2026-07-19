from mpi4py import MPI
import random
import math

# --- 程序1：流体动力学状态分析 (Ranks 0-3) ---
FLUID_DYNAMICS_TYPE_DEF = {
    'A0': '流场稳定平衡', 'A1': '动量通量主导', 'A2': '惯性力不足', 'A3': '压力粘性耦合失衡',
    'A4': '动能与压力能比较', 'A5': '速度开方与雷诺数关系', 'A6': '流速分段与密度交互', 'A7': '多变量倒数和判据',
    'B0': '压力密度速度平衡', 'B1': '静压超标', 'B2': '动量压力失配', 'B3': '高压驱动异常',
    'B4': '速度平方与压力比', 'B5': '压力开方与密度线性组合', 'B6': '动量除以压力开方',
    'C0': '粘性效应平衡', 'C1': '运动粘度过高', 'C2': '压力粘度平方和异常', 'C3': '粘密耦合主导',
    'C4': '压力密度几何平均', 'C5': '压力平方加粘度密度积',
    'D0': '湍流转捩平衡', 'D1': '惯性项不足', 'D2': '低雷诺数失稳', 'D3': '共振转捩条件',
    'D4': '密度粘度积与雷诺数比', 'D5': '雷诺数开方与密度粘度和', 'D6': '粘度雷诺数分数幂积',
}

# --- 程序2：热传导状态分析 (Ranks 4-7) ---
HEAT_TRANSFER_TYPE_DEF = {
    'A0': '宏观热平衡', 'A1': '温度平方效应主导', 'A2': '材料热响应不足', 'A3': '温导耦合弱化',
    'A4': '温度热流乘积与材料性能比', 'A5': '温度开方与扩散率关系', 'A6': '温度分段与热流交互', 'A7': '多变量倒数和判据',
    'B0': '温度热流导热平衡', 'B1': 'Fourier定律偏离', 'B2': '导温比异常', 'B3': '温热耦合超限',
    'B4': '温度平方与热流导热比', 'B5': '热流开方与导热线性组合', 'B6': '温度热流除以导热开方',
    'C0': '材料热性能平衡', 'C1': '热流平方主导', 'C2': '高比热材料', 'C3': '热性能失配',
    'C4': '热流导热几何平均', 'C5': '热流平方加导热比热积',
    'D0': '瞬态热冲击平衡', 'D1': '超快扩散', 'D2': '蓄热超速', 'D3': '导热主导模式',
    'D4': '导热比热积与扩散率比', 'D5': '扩散率开方与导热比热和', 'D6': '比热扩散率分数幂积',
}

# --- 程序3：量子态状态分析 (Ranks 8-11) ---
QUANTUM_MECHANICS_TYPE_DEF = {
    'A0': '量子态稳定平衡', 'A1': '概率密度高阶矩主导', 'A2': '量子态密度超限', 'A3': '精细结构失衡',
    'A4': '概率密度能量乘积与势能量子数比', 'A5': '能量平方开方与量子数关系',
    'B0': '波函数能量势能平衡', 'B1': '自由粒子态', 'B2': '波函数能量响应异常', 'B3': '深势阱束缚态',
    'B4': '概率密度平方与能量势能差平方', 'B5': '能量平方开方与势能线性组合', 'B6': '概率能量平方除以势能平方开方',
    'C0': '能级结构平衡', 'C1': '准连续谱特征', 'C2': '弱耦合谐振子', 'C3': '能量主导演化',
    'C4': '能量势能平方和开方', 'C5': '能量平方加势能间隔积', 'C6': '能量势能差平方开方加间隔', 'C7': '三变量平方分数幂和',
    'D0': '量子隧穿平衡', 'D1': '隧穿抑制态', 'D2': '类氢原子能级结构', 'D3': '偶宇称深束缚态',
    'D4': '势能间隔积与量子数比', 'D5': '量子数开方与势能间隔和', 'D6': '间隔量子数分数幂积',
}

# --- 程序4：分子动力学状态分析 (Ranks 12-15) ---
MOLECULAR_DYNAMICS_TYPE_DEF = {
    'A0': '系综平衡态', 'A1': '热运动尺度失衡', 'A2': '压力温度比异常', 'A3': 'Lennard-Jones排斥主导',
    'A4': '间距速度乘积与温度压力比', 'A5': '温度开方与压力关系', 'A6': '间距分段与速度交互',
    'B0': '空间动力学平衡', 'B1': '归一化动能超标', 'B2': '强相互作用慢速区', 'B3': '热运动特征长度主导',
    'B4': '速度平方与间距温度比', 'B5': '温度开方与间距线性组合', 'B6': '间距速度除以温度开方',
    'C0': '热力学状态平衡', 'C1': '固相特征态', 'C2': '势能平方主导', 'C3': '强相互作用非线性',
    'C4': '速度温度几何平均', 'C5': '速度平方加温度势能积', 'C6': '速度温度差平方开方', 'C7': '三变量分数幂和',
    'D0': '结构稳定性平衡', 'D1': '凝聚态判据', 'D2': '压力势能耦合主导', 'D3': '势能二次效应主导',
    'D4': '温度势能积与压力比', 'D5': '压力开方与温度势能和', 'D6': '势能压力分数幂积', 'D7': '温度势能平方差除以压力',
}

# --- 程序5：天体运动状态分析 (Ranks 16-19) ---
CELESTIAL_MECHANICS_TYPE_DEF = {
    'A0': '轨道稳定平衡', 'A1': '轨道速度一致性失衡', 'A2': '小质量快速轨道', 'A3': '角动量失衡',
    'A4': '半径速度积与质量比', 'A5': '质量与角速度开方比较', 'A6': '半径质量积与速度比', 'A7': '多变量倒数和',
    'B0': '位置速度质量平衡', 'B1': '轨道能量异常', 'B2': '外太阳系大质量天体', 'B3': '大轨道慢速模式',
    'B4': '速度平方与半径质量积', 'B5': '质量开方与半径速度和', 'B6': '半径速度与质量开方比', 'B7': '半径速度分数幂和',
    'C0': '轨道形态平衡', 'C1': '近圆轨道特征', 'C2': '椭圆慢速轨道', 'C3': '彗星型轨道',
    'C4': '速度质量几何平均', 'C5': '速度平方加质量离心率积', 'C6': '速度质量差平方开方',
    'D0': '引力角动量平衡', 'D1': '大质量主导系统', 'D2': '轨道参数和主导', 'D3': '快速圆轨道共轨态',
    'D4': '质量离心率积与角速度比', 'D5': '角速度开方与质量离心率和', 'D6': '离心率角速度分数幂积',
}

# --- 程序6：材料应力状态分析 (Ranks 20-23) ---
MATERIAL_STRESS_TYPE_DEF = {
    'A0': '力学响应平衡', 'A1': '胡克定律偏离', 'A2': '剪切主导或不可压缩材料', 'A3': '总应力状态异常',
    'A4': '应力应变积与模量比', 'A5': '模量开方与泊松比关系', 'A6': '应力模量积与剪切比', 'A7': '多变量倒数和',
    'B0': '应力应变模量平衡', 'B1': '弹性变形高灵敏度', 'B2': '刚性材料特征', 'B3': '本构关系严重偏离',
    'B4': '应力平方与应变模量积', 'B5': '模量开方与应力应变和', 'B6': '应力应变与模量开方比', 'B7': '应力应变分数幂和',
    'C0': '材料性能参数平衡', 'C1': '高模量材料', 'C2': '过刚性材料', 'C3': '低刚度高泊松比材料',
    'C4': '应变模量几何平均', 'C5': '应变平方加模量泊松比积', 'C6': '应变模量差平方开方', 'C7': '三变量分数幂和',
    'D0': '破坏准则平衡', 'D1': '剪切破坏判据', 'D2': '剪切模量不足', 'D3': '剪切主导破坏模式',
    'D4': '模量泊松比积与剪切比', 'D5': '剪切开方与模量泊松比和', 'D6': '泊松剪切分数幂积',
}

def main():
    # 移除了强制 UTF-8 编码的代码，让 Python 自动使用系统的默认编码 (Windows 下通常是 GBK)
    # 之前崩溃是因为有特殊符号，现在特殊符号已经被替换，所以可以安全使用 GBK

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    status = MPI.Status()

    if size != 24:
        if rank == 0:
            print(f"警告：此程序最终设计为 24 个进程，但当前启动了 {size} 个。")
            print("程序将只运行已实现的部分。")

    # -----------------------------------------------------------------
    # --- 程序1：流体动力学状态分析 (Ranks 0-3) ---
    # -----------------------------------------------------------------
    if rank == 0:
        x = random.uniform(0.1, 50.0)  # 流速 v (m/s)
        y = random.uniform(10.0, 1000.0)  # 压力 p (kPa)
        z = random.uniform(1.0, 1000.0)  # 密度 ρ (kg/m^3)
        w = random.uniform(0.1, 100.0)  # 动力粘度 μ (mPa·s)
        m = random.uniform(1.0, 10000.0)  # 雷诺数 Re

        comm.send(x, dest=1, tag=1); comm.send(y, dest=1, tag=2); comm.send(z, dest=1, tag=3)
        comm.send(y, dest=2, tag=1); comm.send(z, dest=2, tag=2); comm.send(w, dest=2, tag=3)
        comm.send(z, dest=3, tag=1); comm.send(w, dest=3, tag=2); comm.send(m, dest=3, tag=3)

        type_code = 'A0'
        analysis_detail = ""

        if x * z > y / 5 + w * 10:
            type_code = 'A1'
            momentum_flux = x * z
            pressure_viscous_resistance = y / 5 + w * 10
            flux_dominance = momentum_flux - pressure_viscous_resistance
            dominance_ratio = momentum_flux / pressure_viscous_resistance if pressure_viscous_resistance > 0 else float('inf')
            convection_instability = min(dominance_ratio * 18, 100)
            analysis_detail = f"动量通量主导分析: 动量通量={momentum_flux:.2f}, 压粘阻力={pressure_viscous_resistance:.2f}, 通量主导度={flux_dominance:.2f}, 主导比={dominance_ratio:.3f}, 对流不稳定性={convection_instability:.1f}%"

        if m + w * 50 < x * 100:
            type_code = 'A2'
            reynolds_viscous_capacity = m + w * 50
            velocity_inertial_demand = x * 100
            capacity_deficit = velocity_inertial_demand - reynolds_viscous_capacity
            inertial_insufficiency = capacity_deficit / reynolds_viscous_capacity if reynolds_viscous_capacity > 0 else float('inf')
            flow_support_gap = min(inertial_insufficiency * 24, 95)
            analysis_detail = f"惯性力不足分析: 雷诺粘性容量={reynolds_viscous_capacity:.2f}, 速度惯性需求={velocity_inertial_demand:.2f}, 容量缺口={capacity_deficit:.2f}, 惯性不足度={inertial_insufficiency:.3f}, 流动支撑缺口={flow_support_gap:.1f}%"

        if y * w < x * z + 5000:
            type_code = 'A3'
            pressure_viscous_coupling = y * w
            inertial_baseline = x * z + 5000
            coupling_weakness = inertial_baseline - pressure_viscous_coupling
            imbalance_factor = coupling_weakness / pressure_viscous_coupling if pressure_viscous_coupling > 0 else float('inf')
            coupling_stress = min(imbalance_factor * 15, 95)
            analysis_detail = f"压粘耦合失衡分析: 压粘耦合度={pressure_viscous_coupling:.2f}, 惯性基准值={inertial_baseline:.2f}, 耦合弱化量={coupling_weakness:.2f}, 失衡因子={imbalance_factor:.3f}, 耦合应力={coupling_stress:.1f}%"

        if x ** 2 * z > y * 100 + w * m:
            type_code = 'A4'
            kinetic_energy_term = x ** 2 * z
            pressure_viscous_term = y * 100 + w * m
            analysis_detail = f"动能与压力能比较分析: 动能项={kinetic_energy_term:.2f}, 压粘项={pressure_viscous_term:.2f}, 能量失衡度={min((kinetic_energy_term - pressure_viscous_term) / pressure_viscous_term * 20, 95) if pressure_viscous_term > 0 else 0:.1f}%"

        if (x + y / 10) ** 0.5 < (m / 20 + z / 50) ** 0.5:
            type_code = 'A5'
            velocity_pressure_root = (x + y / 10) ** 0.5
            reynolds_density_root = (m / 20 + z / 50) ** 0.5
            analysis_detail = f"速度开方与雷诺数关系分析: 速压开方={velocity_pressure_root:.2f}, 雷密开方={reynolds_density_root:.2f}, 开方缺口度={min((reynolds_density_root - velocity_pressure_root) / velocity_pressure_root * 28, 95) if velocity_pressure_root > 0 else 0:.1f}%"

        if (x // 10) * z + (x % 10) * w > y + m * 50:
            type_code = 'A6'
            segmented_interaction = (x // 10) * z + (x % 10) * w
            pressure_reynolds_baseline = y + m * 50
            analysis_detail = f"流速分段与密度交互分析: 分段交互值={segmented_interaction:.2f}, 压雷基线={pressure_reynolds_baseline:.2f}, 分段超载度={min((segmented_interaction - pressure_reynolds_baseline) / pressure_reynolds_baseline * 22, 95) if pressure_reynolds_baseline > 0 else 0:.1f}%"

        if x / (y + 10) + z / (w + 10) > m / 100 + 5:
            type_code = 'A7'
            reciprocal_sum = x / (y + 10) + z / (w + 10)
            reynolds_threshold = m / 100 + 5
            analysis_detail = f"多变量倒数和判据分析: 倒数和={reciprocal_sum:.3f}, 雷诺阈值={reynolds_threshold:.2f}, 倒数和异常度={min((reciprocal_sum - reynolds_threshold) / reynolds_threshold * 25, 95):.1f}%"

        pressure_density_result = comm.recv(source=1, tag=100, status=status)
        viscous_effect_result = comm.recv(source=2, tag=200, status=status)
        turbulence_result = comm.recv(source=3, tag=300, status=status)

        analysis_results = [
            f"宏观流场稳定性 (v,p,ρ,μ,Re): {type_code} -> {FLUID_DYNAMICS_TYPE_DEF.get(type_code, '未知')} | {analysis_detail}",
            f"压力密度速度耦合 (v,p,ρ): {pressure_density_result['code']} -> {FLUID_DYNAMICS_TYPE_DEF.get(pressure_density_result['code'], '未知')} | {pressure_density_result['detail']}",
            f"粘性效应分析 (p,ρ,μ): {viscous_effect_result['code']} -> {FLUID_DYNAMICS_TYPE_DEF.get(viscous_effect_result['code'], '未知')} | {viscous_effect_result['detail']}",
            f"湍流转捩判断 (ρ,μ,Re): {turbulence_result['code']} -> {FLUID_DYNAMICS_TYPE_DEF.get(turbulence_result['code'], '未知')} | {turbulence_result['detail']}"
        ]

        print("=" * 75)
        print("  流体动力学模拟系统 (进程 0-3)  ")
        print("=" * 75)
        print()
        print("--- 实时流场参数 ---")
        print(f"流速 v (X): {x:.3f} m/s")
        print(f"压力 p (Y): {y:.2f} kPa")
        print(f"密度 ρ (Z): {z:.2f} kg/m^3")
        print(f"动力粘度 μ (W): {w:.3f} mPa·s")
        print(f"雷诺数 Re (M): {m:.1f}")
        print()
        print("--- 流场综合分析报告 ---")
        for i, result in enumerate(analysis_results, 1):
            print(f"{i}. {result}")
        print()
        print("=" * 75)
        print(f"程序1 (Ranks 0-3) 分析完成")
        print("=" * 75)
        print("\n")

    elif rank == 1:
        x = comm.recv(source=0, tag=1, status=status)
        y = comm.recv(source=0, tag=2, status=status)
        z = comm.recv(source=0, tag=3, status=status)

        type_code = 'B0'
        analysis_detail = ""

        if y > x * x * z / 3 + 150:
            type_code = 'B1'
            static_pressure = y
            dynamic_pressure_threshold = x ** 2 * z / 3 + 150
            pressure_excess = static_pressure - dynamic_pressure_threshold
            pressure_imbalance = pressure_excess / dynamic_pressure_threshold if dynamic_pressure_threshold > 0 else float('inf')
            static_dominance_level = min(pressure_imbalance * 28, 95)
            analysis_detail = f"静压超标分析: 静压={static_pressure:.2f}kPa, 动压阈值={dynamic_pressure_threshold:.2f}kPa, 压力超量={pressure_excess:.2f}kPa, 压力失衡度={pressure_imbalance:.3f}, 静压主导程度={static_dominance_level:.1f}%"

        if x * z > y * y / 80:
            type_code = 'B2'
            momentum_magnitude = x * z
            pressure_squared_scale = y ** 2 / 80
            momentum_overflow = momentum_magnitude - pressure_squared_scale
            scale_amplification = momentum_magnitude / pressure_squared_scale if pressure_squared_scale > 0 else float('inf')
            momentum_pressure_mismatch = min(scale_amplification * 19, 95)
            analysis_detail = f"动量压力失配分析: 动量量级={momentum_magnitude:.2f}, 压力平方标度={pressure_squared_scale:.2f}, 动量溢出={momentum_overflow:.2f}, 标度放大倍数={scale_amplification:.3f}, 动压失配度={momentum_pressure_mismatch:.1f}%"

        if x > (y - 100) / z * 4 and y > 200:
            type_code = 'B3'
            flow_velocity = x
            density_adjusted_limit = (y - 100) / z * 4 if z > 0 else 0
            high_pressure_regime = y
            velocity_surplus = flow_velocity - density_adjusted_limit
            driving_efficiency = high_pressure_regime / (flow_velocity * z) if (flow_velocity * z) > 0 else 0
            high_pressure_anomaly = 100 - min(velocity_surplus / 2 + driving_efficiency / 5, 88)
            analysis_detail = f"高压驱动异常分析: 流速={flow_velocity:.2f}m/s, 密度调整上限={density_adjusted_limit:.2f}m/s, 高压区间={high_pressure_regime:.2f}kPa, 速度盈余={velocity_surplus:.2f}m/s, 驱动效率={driving_efficiency:.3f}, 高压异常度={high_pressure_anomaly:.1f}%"

        if x ** 2 > y * z / 20 + 500:
            type_code = 'B4'
            velocity_squared = x ** 2
            pressure_density_scaled = y * z / 20 + 500
            analysis_detail = f"速度平方与压力比分析: 速度平方={velocity_squared:.2f}, 压密缩放={pressure_density_scaled:.2f}, 速度平方超载度={min((velocity_squared - pressure_density_scaled) / pressure_density_scaled * 21, 95) if pressure_density_scaled > 0 else 0:.1f}%"

        if y ** 0.5 + z / 10 < x * 3 + 15:
            type_code = 'B5'
            pressure_root_density = y ** 0.5 + z / 10
            velocity_linear_baseline = x * 3 + 15
            analysis_detail = f"压力开方与密度线性组合分析: 压力开方密度={pressure_root_density:.2f}, 速度线性基线={velocity_linear_baseline:.2f}, 组合缺口度={min((velocity_linear_baseline - pressure_root_density) / pressure_root_density * 30, 95) if pressure_root_density > 0 else 0:.1f}%"

        if x * z / (y ** 0.5 + 1) > 200:
            type_code = 'B6'
            momentum_pressure_ratio = x * z / (y ** 0.5 + 1)
            ratio_threshold = 200
            analysis_detail = f"动量除以压力开方分析: 动量压力比={momentum_pressure_ratio:.2f}, 比值阈值={ratio_threshold}, 比值超载度={min((momentum_pressure_ratio - ratio_threshold) / ratio_threshold * 18, 95):.1f}%"

        result = {'code': type_code, 'detail': analysis_detail}
        comm.send(result, dest=0, tag=100)

    elif rank == 2:
        y = comm.recv(source=0, tag=1, status=status)
        z = comm.recv(source=0, tag=2, status=status)
        w = comm.recv(source=0, tag=3, status=status)

        type_code = 'C0'
        analysis_detail = ""

        if w / z > y / 800:
            type_code = 'C1'
            kinematic_viscosity = w / z if z > 0 else 0
            pressure_ratio_criterion = y / 800
            viscosity_excess = kinematic_viscosity - pressure_ratio_criterion
            viscous_dominance = viscosity_excess / pressure_ratio_criterion if pressure_ratio_criterion > 0 else float('inf')
            kinematic_anomaly_level = min(viscous_dominance * 35, 95)
            # 修复: m^2/s
            analysis_detail = f"运动粘度过高分析: 运动粘度={kinematic_viscosity:.4f}m^2/s, 压力比判据={pressure_ratio_criterion:.4f}, 粘度超量={viscosity_excess:.4f}, 粘性主导度={viscous_dominance:.3f}, 运动粘度异常程度={kinematic_anomaly_level:.1f}%"

        if y * y + w * w > z * 500:
            type_code = 'C2'
            pressure_viscosity_quadratic = y ** 2 + w ** 2
            density_capacity_limit = z * 500
            quadratic_overload = pressure_viscosity_quadratic - density_capacity_limit
            capacity_strain = quadratic_overload / density_capacity_limit if density_capacity_limit > 0 else float('inf')
            squared_sum_anomaly = min(capacity_strain * 23, 95)
            analysis_detail = f"压粘平方和异常分析: 压粘二次方和={pressure_viscosity_quadratic:.2f}, 密度容量限={density_capacity_limit:.2f}, 二次过载量={quadratic_overload:.2f}, 容量应变度={capacity_strain:.3f}, 平方和异常程度={squared_sum_anomaly:.1f}%"

        if w * z > y * 35 + 1800:
            type_code = 'C3'
            viscous_density_coupling = w * z
            pressure_driving_baseline = y * 35 + 1800
            coupling_dominance = viscous_density_coupling - pressure_driving_baseline
            viscous_density_imbalance = coupling_dominance / pressure_driving_baseline if pressure_driving_baseline > 0 else float('inf')
            coupling_dominance_level = min(viscous_density_imbalance * 17, 95)
            analysis_detail = f"粘密耦合主导分析: 粘密耦合度={viscous_density_coupling:.2f}, 压力驱动基准={pressure_driving_baseline:.2f}, 耦合主导量={coupling_dominance:.2f}, 粘密失衡度={viscous_density_imbalance:.3f}, 耦合主导程度={coupling_dominance_level:.1f}%"

        if (y * z) ** 0.5 < w * 15 + 100:
            type_code = 'C4'
            pressure_density_geometric = (y * z) ** 0.5
            viscosity_baseline = w * 15 + 100
            analysis_detail = f"压力密度几何平均分析: 压密几何平均={pressure_density_geometric:.2f}, 粘度基线={viscosity_baseline:.2f}, 几何平均不足度={min((viscosity_baseline - pressure_density_geometric) / pressure_density_geometric * 27, 95) if pressure_density_geometric > 0 else 0:.1f}%"

        if y ** 2 / 100 + w * z > 1500:
            type_code = 'C5'
            pressure_viscous_aggregate = y ** 2 / 100 + w * z
            aggregate_threshold = 1500
            analysis_detail = f"压力平方加粘度密度积分析: 压粘聚合值={pressure_viscous_aggregate:.2f}, 聚合阈值={aggregate_threshold}, 聚合超载度={min((pressure_viscous_aggregate - aggregate_threshold) / aggregate_threshold * 23, 95):.1f}%"

        result = {'code': type_code, 'detail': analysis_detail}
        comm.send(result, dest=0, tag=200)

    elif rank == 3:
        z = comm.recv(source=0, tag=1, status=status)
        w = comm.recv(source=0, tag=2, status=status)
        m = comm.recv(source=0, tag=3, status=status)

        type_code = 'D0'
        analysis_detail = ""

        if z * m < w * 150:
            type_code = 'D1'
            inertial_term = z * m
            viscous_resistance_threshold = w * 150
            inertial_deficiency = viscous_resistance_threshold - inertial_term
            resistance_dominance = inertial_deficiency / inertial_term if inertial_term > 0 else float('inf')
            inertial_insufficiency_degree = min(resistance_dominance * 27, 95)
            analysis_detail = f"惯性项不足分析: 惯性项={inertial_term:.2f}, 粘阻阈值={viscous_resistance_threshold:.2f}, 惯性亏缺={inertial_deficiency:.2f}, 阻力主导度={resistance_dominance:.3f}, 惯性不足程度={inertial_insufficiency_degree:.1f}%"

        if z + w * 4 > m / 3 + 600:
            type_code = 'D2'
            density_viscosity_combination = z + w * 4
            low_reynolds_stability_limit = m / 3 + 600
            combination_overflow = density_viscosity_combination - low_reynolds_stability_limit
            instability_factor = combination_overflow / low_reynolds_stability_limit if low_reynolds_stability_limit > 0 else float('inf')
            low_reynolds_instability = min(instability_factor * 21, 95)
            analysis_detail = f"低雷诺数失稳分析: 密粘组合值={density_viscosity_combination:.2f}, 低Re稳定限={low_reynolds_stability_limit:.2f}, 组合溢出={combination_overflow:.2f}, 失稳因子={instability_factor:.3f}, 低Re失稳度={low_reynolds_instability:.1f}%"

        if (z - w) % 50 < m / 200:
            type_code = 'D3'
            density_viscosity_difference = z - w
            periodic_remainder = density_viscosity_difference % 50
            reynolds_scale_threshold = m / 200
            resonance_proximity = reynolds_scale_threshold - periodic_remainder
            synchronization_index = min((50 - periodic_remainder) / 5 + m / 1000, 95)
            analysis_detail = f"共振转捩条件分析: 密粘差值={density_viscosity_difference:.2f}, 周期余数={periodic_remainder:.2f}, 雷诺尺度阈值={reynolds_scale_threshold:.2f}, 共振接近度={resonance_proximity:.2f}, 同步指数={synchronization_index:.1f}%"

        if z * w / (m + 100) > 8:
            type_code = 'D4'
            density_viscosity_ratio = z * w / (m + 100)
            ratio_threshold = 8
            analysis_detail = f"密度粘度积与雷诺数比分析: 密粘雷比={density_viscosity_ratio:.2f}, 比值阈值={ratio_threshold}, 比值超载度={min((density_viscosity_ratio - ratio_threshold) / ratio_threshold * 25, 95):.1f}%"

        if m ** 0.5 < z / 10 + w * 2 + 20:
            type_code = 'D5'
            reynolds_root = m ** 0.5
            density_viscosity_sum = z / 10 + w * 2 + 20
            analysis_detail = f"雷诺数开方与密度粘度和分析: 雷诺开方={reynolds_root:.2f}, 密粘和={density_viscosity_sum:.2f}, 雷诺不足度={min((density_viscosity_sum - reynolds_root) / reynolds_root * 31, 95) if reynolds_root > 0 else 0:.1f}%"

        if w ** 0.6 * m ** 0.4 > z * 100 + 1000:
            type_code = 'D6'
            viscosity_reynolds_power = w ** 0.6 * m ** 0.4
            density_baseline = z * 100 + 1000
            analysis_detail = f"粘度雷诺数分数幂积分析: 粘雷幂积={viscosity_reynolds_power:.2f}, 密度基线={density_baseline:.2f}, 幂积超载度={min((viscosity_reynolds_power - density_baseline) / density_baseline * 20, 95) if density_baseline > 0 else 0:.1f}%"

        result = {'code': type_code, 'detail': analysis_detail}
        comm.send(result, dest=0, tag=300)

    # -----------------------------------------------------------------
    # --- 程序2：热传导状态分析 (Ranks 4-7) ---
    # -----------------------------------------------------------------
    elif rank == 4:
        x = random.uniform(200.0, 2000.0)  # 温度 T (K)
        y = random.uniform(0.1, 1000.0)  # 热流密度 q (kW/m^2)
        z = random.uniform(0.1, 500.0)  # 导热系数 k (W/(m·K))
        w = random.uniform(0.1, 5.0)  # 比热容 c (kJ/(kg·K))
        m = random.uniform(0.01, 100.0)  # 热扩散率 α (mm^2/s)

        comm.send(x, dest=5, tag=1); comm.send(y, dest=5, tag=2); comm.send(z, dest=5, tag=3)
        comm.send(y, dest=6, tag=1); comm.send(z, dest=6, tag=2); comm.send(w, dest=6, tag=3)
        comm.send(z, dest=7, tag=1); comm.send(w, dest=7, tag=2); comm.send(m, dest=7, tag=3)

        type_code = 'A0'
        analysis_detail = ""

        if x * x / 1000 > y + z * 2:
            type_code = 'A1'
            temperature_squared_effect = x ** 2 / 1000
            conduction_radiation_baseline = y + z * 2
            nonlinear_dominance = temperature_squared_effect - conduction_radiation_baseline
            quadratic_amplification = temperature_squared_effect / conduction_radiation_baseline if conduction_radiation_baseline > 0 else float('inf')
            radiation_contribution_ratio = min(quadratic_amplification * 12, 100)
            analysis_detail = f"温度二次效应分析: 温度平方项={temperature_squared_effect:.2f}, 传导辐射基线={conduction_radiation_baseline:.2f}, 非线性主导度={nonlinear_dominance:.2f}, 二次放大系数={quadratic_amplification:.3f}, 辐射贡献率={radiation_contribution_ratio:.1f}%"

        if w * m * 100 < x / 8 + y / 50:
            type_code = 'A2'
            material_thermal_response = w * m * 100
            temperature_flux_demand = x / 8 + y / 50
            response_deficiency = temperature_flux_demand - material_thermal_response
            inadequacy_factor = response_deficiency / material_thermal_response if material_thermal_response > 0 else float('inf')
            thermal_lag_severity = min(inadequacy_factor * 28, 95)
            analysis_detail = f"材料响应不足分析: 材料热响应能力={material_thermal_response:.3f}, 温热流需求={temperature_flux_demand:.2f}, 响应亏缺={response_deficiency:.2f}, 不足因子={inadequacy_factor:.3f}, 热滞后严重度={thermal_lag_severity:.1f}%"

        if x / (w + 0.01) > z * 5 + y / 8:
            type_code = 'A3'
            temperature_specific_ratio = x / (w + 0.01)
            dissipation_capacity_index = z * 5 + y / 8
            thermal_potential_excess = temperature_specific_ratio - dissipation_capacity_index
            heat_retention_dominance = thermal_potential_excess / dissipation_capacity_index if dissipation_capacity_index > 0 else float('inf')
            energy_accumulation_risk = min(heat_retention_dominance * 16, 95)
            analysis_detail = f"温热潜力过剩分析: 温度比热比={temperature_specific_ratio:.2f}K/(kJ/kg), 散热容量指数={dissipation_capacity_index:.2f}, 热潜力盈余={thermal_potential_excess:.2f}, 热滞留主导度={heat_retention_dominance:.3f}, 能量累积风险={energy_accumulation_risk:.1f}%"

        if x * y / 100 > z * w * m + 500:
            type_code = 'A4'
            temperature_flux_product = x * y / 100
            material_thermal_capacity = z * w * m + 500
            analysis_detail = f"温度热流乘积与材料性能比分析: 温热积={temperature_flux_product:.2f}, 材料热容量={material_thermal_capacity:.2f}, 积超载度={min((temperature_flux_product - material_thermal_capacity) / material_thermal_capacity * 19, 95) if material_thermal_capacity > 0 else 0:.1f}%"

        if x ** 0.5 < (m * 10 + z / 10) ** 0.5 + w * 5:
            type_code = 'A5'
            temperature_root = x ** 0.5
            diffusion_conductivity_root = (m * 10 + z / 10) ** 0.5 + w * 5
            analysis_detail = f"温度开方与扩散率关系分析: 温度开方={temperature_root:.2f}, 扩散导热开方={diffusion_conductivity_root:.2f}, 开方缺口度={min((diffusion_conductivity_root - temperature_root) / temperature_root * 25, 95) if temperature_root > 0 else 0:.1f}%"

        if (x // 100) * y + (x % 100) * z > w * m * 100 + 1000:
            type_code = 'A6'
            segmented_thermal_interaction = (x // 100) * y + (x % 100) * z
            capacity_diffusion_baseline = w * m * 100 + 1000
            analysis_detail = f"温度分段与热流交互分析: 分段热交互={segmented_thermal_interaction:.2f}, 容扩基线={capacity_diffusion_baseline:.2f}, 分段超载度={min((segmented_thermal_interaction - capacity_diffusion_baseline) / capacity_diffusion_baseline * 21, 95) if capacity_diffusion_baseline > 0 else 0:.1f}%"

        if x / (y + 10) + z / (w + 0.1) > m * 2 + 50:
            type_code = 'A7'
            reciprocal_thermal_sum = x / (y + 10) + z / (w + 0.1)
            diffusivity_threshold = m * 2 + 50
            analysis_detail = f"多变量倒数和判据分析: 倒数热和={reciprocal_thermal_sum:.2f}, 扩散阈值={diffusivity_threshold:.2f}, 倒数和异常度={min((reciprocal_thermal_sum - diffusivity_threshold) / diffusivity_threshold * 23, 95):.1f}%"

        temperature_flux_result = comm.recv(source=5, tag=100, status=status)
        material_property_result = comm.recv(source=6, tag=200, status=status)
        transient_shock_result = comm.recv(source=7, tag=300, status=status)

        analysis_results = [
            f"宏观热平衡 (T,q,k,c,α): {type_code} -> {HEAT_TRANSFER_TYPE_DEF.get(type_code, '未知')} | {analysis_detail}",
            f"温度热流导热 (T,q,k): {temperature_flux_result['code']} -> {HEAT_TRANSFER_TYPE_DEF.get(temperature_flux_result['code'], '未知')} | {temperature_flux_result['detail']}",
            f"材料热性能 (q,k,c): {material_property_result['code']} -> {HEAT_TRANSFER_TYPE_DEF.get(material_property_result['code'], '未知')} | {material_property_result['detail']}",
            f"瞬态热冲击 (k,c,α): {transient_shock_result['code']} -> {HEAT_TRANSFER_TYPE_DEF.get(transient_shock_result['code'], '未知')} | {transient_shock_result['detail']}"
        ]

        print("=" * 75)
        print("  热传导分析系统 (进程 4-7)  ")
        print("=" * 75)
        print()
        print("--- 实时热学参数 ---")
        print(f"温度 T (X): {x:.2f} K")
        print(f"热流密度 q (Y): {y:.2f} kW/m^2")
        print(f"导热系数 k (Z): {z:.2f} W/(m·K)")
        print(f"比热容 c (W): {w:.3f} kJ/(kg·K)")
        print(f"热扩散率 α (M): {m:.3f} mm^2/s")
        print()
        print("--- 热场综合分析报告 ---")
        for i, result in enumerate(analysis_results, 1):
            print(f"{i}. {result}")
        print()
        print("=" * 75)
        print(f"程序2 (Ranks 4-7) 分析完成")
        print("=" * 75)
        print("\n")

    elif rank == 5:
        x = comm.recv(source=4, tag=1, status=status)
        y = comm.recv(source=4, tag=2, status=status)
        z = comm.recv(source=4, tag=3, status=status)

        type_code = 'B0'
        analysis_detail = ""

        if (y - z) * (y + z) > x * 80:
            type_code = 'B1'
            flux_conductivity_difference = y - z
            flux_conductivity_sum = y + z
            quadratic_difference_effect = flux_conductivity_difference * flux_conductivity_sum
            temperature_scaling_threshold = x * 80
            thermal_imbalance_magnitude = quadratic_difference_effect - temperature_scaling_threshold
            quadratic_asymmetry_factor = quadratic_difference_effect / temperature_scaling_threshold if temperature_scaling_threshold > 0 else float('inf')
            heat_accumulation_criticality = min(quadratic_asymmetry_factor * 21, 95)
            analysis_detail = f"二次差异效应分析: 热流导热差={flux_conductivity_difference:.2f}, 热流导热和={flux_conductivity_sum:.2f}, 二次差异效应={quadratic_difference_effect:.2f}, 温度标度阈值={temperature_scaling_threshold:.2f}, 热失衡幅度={thermal_imbalance_magnitude:.2f}, 二次不对称因子={quadratic_asymmetry_factor:.3f}, 热量堆积临界性={heat_accumulation_criticality:.1f}%"

        if z / x > y ** 3 / 1000000:
            type_code = 'B2'
            conductivity_temperature_ratio = z / x if x > 0 else 0
            flux_cubic_microscale = y ** 3 / 1000000
            ratio_excess = conductivity_temperature_ratio - flux_cubic_microscale
            microscale_amplification = conductivity_temperature_ratio / flux_cubic_microscale if flux_cubic_microscale > 0 else float('inf')
            multiscale_coupling_anomaly = min(microscale_amplification * 16, 95)
            analysis_detail = f"导温比异常分析: 导温比={conductivity_temperature_ratio:.4f}, 热流立方微尺度={flux_cubic_microscale:.6f}, 比值超量={ratio_excess:.4f}, 微尺度放大倍数={microscale_amplification:.2f}, 多尺度耦合异常={multiscale_coupling_anomaly:.1f}%"

        if x * y > z * z * 500 + 100000:
            type_code = 'B3'
            temperature_flux_coupling = x * y
            conductivity_squared_limit = z ** 2 * 500 + 100000
            coupling_overflow = temperature_flux_coupling - conductivity_squared_limit
            material_limit_violation = coupling_overflow / conductivity_squared_limit if conductivity_squared_limit > 0 else float('inf')
            thermal_overload_severity = min(material_limit_violation * 18, 95)
            analysis_detail = f"温热耦合超限分析: 温热耦合强度={temperature_flux_coupling:.2f}, 导热平方极限={conductivity_squared_limit:.2f}, 耦合溢出量={coupling_overflow:.2f}, 材料极限违背度={material_limit_violation:.3f}, 热过载严重度={thermal_overload_severity:.1f}%"

        if x ** 2 / 1000 > y * z + 300:
            type_code = 'B4'
            temperature_squared_scaled = x ** 2 / 1000
            flux_conductivity_product = y * z + 300
            analysis_detail = f"温度平方与热流导热比分析: 温度平方缩放={temperature_squared_scaled:.2f}, 热流导热积={flux_conductivity_product:.2f}, 平方超载度={min((temperature_squared_scaled - flux_conductivity_product) / flux_conductivity_product * 20, 95) if flux_conductivity_product > 0 else 0:.1f}%"

        if y ** 0.5 + z / 10 < x / 20 + 30:
            type_code = 'B5'
            flux_root_conductivity = y ** 0.5 + z / 10
            temperature_linear_baseline = x / 20 + 30
            analysis_detail = f"热流开方与导热线性组合分析: 热流开方导热={flux_root_conductivity:.2f}, 温度线性基线={temperature_linear_baseline:.2f}, 组合缺口度={min((temperature_linear_baseline - flux_root_conductivity) / flux_root_conductivity * 27, 95) if flux_root_conductivity > 0 else 0:.1f}%"

        if x * y / (z ** 0.5 + 1) > 5000:
            type_code = 'B6'
            temperature_flux_conductivity_ratio = x * y / (z ** 0.5 + 1)
            ratio_threshold = 5000
            analysis_detail = f"温度热流除以导热开方分析: 温热导比={temperature_flux_conductivity_ratio:.2f}, 比值阈值={ratio_threshold}, 比值超载度={min((temperature_flux_conductivity_ratio - ratio_threshold) / ratio_threshold * 17, 95):.1f}%"

        result = {'code': type_code, 'detail': analysis_detail}
        comm.send(result, dest=4, tag=100)

    elif rank == 6:
        y = comm.recv(source=4, tag=1, status=status)
        z = comm.recv(source=4, tag=2, status=status)
        w = comm.recv(source=4, tag=3, status=status)

        type_code = 'C0'
        analysis_detail = ""

        if y * y > z * w * 800:
            type_code = 'C1'
            flux_squared_effect = y ** 2
            thermal_storage_threshold = z * w * 800
            quadratic_dominance = flux_squared_effect - thermal_storage_threshold
            storage_capacity_strain = quadratic_dominance / thermal_storage_threshold if thermal_storage_threshold > 0 else float('inf')
            flux_intensity_criticality = min(storage_capacity_strain * 22, 95)
            analysis_detail = f"热流平方主导分析: 热流平方项={flux_squared_effect:.2f}, 储热阈值={thermal_storage_threshold:.2f}, 二次主导度={quadratic_dominance:.2f}, 储能容量应变={storage_capacity_strain:.3f}, 通量强度临界性={flux_intensity_criticality:.1f}%"

        if w > (y + z) / 4:
            type_code = 'C2'
            specific_heat_capacity = w
            flux_conductivity_average = (y + z) / 4
            heat_storage_dominance = specific_heat_capacity - flux_conductivity_average
            capacity_proportion = specific_heat_capacity / flux_conductivity_average if flux_conductivity_average > 0 else float('inf')
            thermal_inertia_index = min(capacity_proportion * 30, 95)
            analysis_detail = f"高比热材料分析: 比热容={specific_heat_capacity:.3f}kJ/(kg·K), 通量导热均值={flux_conductivity_average:.2f}, 储热主导度={heat_storage_dominance:.3f}, 容量占比={capacity_proportion:.3f}, 热惯性指数={thermal_inertia_index:.1f}%"

        if z ** 2 + w * y < 1000:
            type_code = 'C3'
            conductivity_squared_gain = z ** 2
            thermal_storage_release_rate = w * y
            combined_thermal_capacity = conductivity_squared_gain + thermal_storage_release_rate
            baseline_thermal_threshold = 1000
            capacity_deficit = baseline_thermal_threshold - combined_thermal_capacity
            performance_inadequacy_ratio = capacity_deficit / baseline_thermal_threshold if baseline_thermal_threshold > 0 else 0
            material_vulnerability_index = min(performance_inadequacy_ratio * 32, 95)
            analysis_detail = f"综合热容量不足分析: 导热系数平方增益={conductivity_squared_gain:.2f}, 热储放速率={thermal_storage_release_rate:.2f}, 综合热容量={combined_thermal_capacity:.2f}, 基准热阈值={baseline_thermal_threshold}, 容量亏缺={capacity_deficit:.2f}, 性能不足率={performance_inadequacy_ratio:.3f}, 材料脆弱性指数={material_vulnerability_index:.1f}%"

        if (y * z) ** 0.5 < w * 50 + 20:
            type_code = 'C4'
            flux_conductivity_geometric = (y * z) ** 0.5
            specific_heat_baseline = w * 50 + 20
            analysis_detail = f"热流导热几何平均分析: 热流导热几何平均={flux_conductivity_geometric:.2f}, 比热基线={specific_heat_baseline:.2f}, 几何平均不足度={min((specific_heat_baseline - flux_conductivity_geometric) / flux_conductivity_geometric * 26, 95) if flux_conductivity_geometric > 0 else 0:.1f}%"

        if y ** 2 / 100 + z * w > 800:
            type_code = 'C5'
            flux_thermal_aggregate = y ** 2 / 100 + z * w
            aggregate_threshold = 800
            analysis_detail = f"热流平方加导热比热积分析: 热流热聚合={flux_thermal_aggregate:.2f}, 聚合阈值={aggregate_threshold}, 聚合超载度={min((flux_thermal_aggregate - aggregate_threshold) / aggregate_threshold * 21, 95):.1f}%"

        result = {'code': type_code, 'detail': analysis_detail}
        comm.send(result, dest=4, tag=200)

    elif rank == 7:
        z = comm.recv(source=4, tag=1, status=status)
        w = comm.recv(source=4, tag=2, status=status)
        m = comm.recv(source=4, tag=3, status=status)

        type_code = 'D0'
        analysis_detail = ""

        if m ** 3 > z * w + 100:
            type_code = 'D1'
            diffusivity_cubed = m ** 3
            conductivity_capacity_baseline = z * w + 100
            cubic_overflow = diffusivity_cubed - conductivity_capacity_baseline
            ultrafast_propagation_ratio = diffusivity_cubed / conductivity_capacity_baseline if conductivity_capacity_baseline > 0 else float('inf')
            transient_shock_intensity = min(ultrafast_propagation_ratio * 15, 95)
            analysis_detail = f"超快扩散分析: 扩散率立方={diffusivity_cubed:.2f}, 导热比热基准={conductivity_capacity_baseline:.2f}, 立方溢出量={cubic_overflow:.2f}, 超快传播比={ultrafast_propagation_ratio:.3f}, 瞬态冲击强度={transient_shock_intensity:.1f}%"

        if z * w / 10 > m + 5:
            type_code = 'D2'
            thermal_storage_rate = z * w / 10
            diffusion_response_capacity = m + 5
            storage_rate_excess = thermal_storage_rate - diffusion_response_capacity
            heat_accumulation_velocity = storage_rate_excess / diffusion_response_capacity if diffusion_response_capacity > 0 else float('inf')
            thermal_buildup_criticality = min(heat_accumulation_velocity * 26, 95)
            analysis_detail = f"蓄热超速分析: 热量储存速率={thermal_storage_rate:.2f}, 扩散响应容量={diffusion_response_capacity:.2f}, 储存速率超量={storage_rate_excess:.2f}, 热量累积速度={heat_accumulation_velocity:.3f}, 热量堆积临界性={thermal_buildup_criticality:.1f}%"

        if z > w * m * 8 + 40:
            type_code = 'D3'
            thermal_conductivity = z
            capacity_diffusivity_threshold = w * m * 8 + 40
            conduction_dominance = thermal_conductivity - capacity_diffusivity_threshold
            steady_state_tendency = conduction_dominance / capacity_diffusivity_threshold if capacity_diffusivity_threshold > 0 else float('inf')
            conduction_regime_intensity = min(steady_state_tendency * 20, 95)
            analysis_detail = f"导热主导模式分析: 导热系数={thermal_conductivity:.2f}W/(m·K), 比热扩散阈值={capacity_diffusivity_threshold:.2f}, 传导主导度={conduction_dominance:.2f}, 稳态倾向性={steady_state_tendency:.3f}, 传导体制强度={conduction_regime_intensity:.1f}%"

        if z * w / (m + 1) > 50:
            type_code = 'D4'
            conductivity_capacity_diffusivity_ratio = z * w / (m + 1)
            ratio_threshold = 50
            analysis_detail = f"导热比热积与扩散率比分析: 导热比热扩散比={conductivity_capacity_diffusivity_ratio:.2f}, 比值阈值={ratio_threshold}, 比值超载度={min((conductivity_capacity_diffusivity_ratio - ratio_threshold) / ratio_threshold * 23, 95):.1f}%"

        if m ** 0.5 < z / 10 + w * 10 + 5:
            type_code = 'D5'
            diffusivity_root = m ** 0.5
            conductivity_capacity_sum = z / 10 + w * 10 + 5
            analysis_detail = f"扩散率开方与导热比热和分析: 扩散率开方={diffusivity_root:.2f}, 导热比热和={conductivity_capacity_sum:.2f}, 扩散不足度={min((conductivity_capacity_sum - diffusivity_root) / diffusivity_root * 29, 95) if diffusivity_root > 0 else 0:.1f}%"

        if w ** 0.6 * m ** 0.5 > z * 5 + 100:
            type_code = 'D6'
            capacity_diffusivity_power = w ** 0.6 * m ** 0.5
            conductivity_baseline = z * 5 + 100
            analysis_detail = f"比热扩散率分数幂积分析: 比热扩散幂积={capacity_diffusivity_power:.2f}, 导热基线={conductivity_baseline:.2f}, 幂积超载度={min((capacity_diffusivity_power - conductivity_baseline) / conductivity_baseline * 19, 95) if conductivity_baseline > 0 else 0:.1f}%"

        result = {'code': type_code, 'detail': analysis_detail}
        comm.send(result, dest=4, tag=300)

    elif rank == 8:
        # 进程8：主进程 (Global Rank 8)：负责数据生成、分发和宏观量子态稳定性分析

        # 1. 随机生成五个核心量子力学变量
        x = random.uniform(0.0, 1.0)  # 概率密度 Ψ^2 (无量纲)
        y = random.uniform(-10.0, 10.0)  # 能量本征值 E (eV)
        z = random.uniform(-5.0, 20.0)  # 势能 V (eV)
        w = random.uniform(0.01, 5.0)  # 能级间隔 ΔE (eV)
        m = random.randint(1, 10)  # 量子数 n (整数)

        comm.send(x, dest=9, tag=1); comm.send(y, dest=9, tag=2); comm.send(z, dest=9, tag=3)
        comm.send(y, dest=10, tag=1); comm.send(z, dest=10, tag=2); comm.send(w, dest=10, tag=3)
        comm.send(z, dest=11, tag=1); comm.send(w, dest=11, tag=2); comm.send(m, dest=11, tag=3)

        type_code = 'A0'
        analysis_detail = ""

        if x ** m > (y + z) / 20:
            type_code = 'A1'
            probability_density = x
            quantum_number = m
            high_order_moment = x ** m
            total_energy_normalized = (y + z) / 20
            moment_dominance = high_order_moment - total_energy_normalized
            concentration_factor = high_order_moment / total_energy_normalized if total_energy_normalized != 0 else float('inf')
            quantum_localization_index = min(concentration_factor * 25, 95)
            analysis_detail = f"高阶矩主导分析: 概率密度={probability_density:.4f}, 量子数={quantum_number}, 高阶矩Ψ^n={high_order_moment:.6f}, 归一化总能量={total_energy_normalized:.3f}, 矩主导度={moment_dominance:.6f}, 集中因子={concentration_factor:.4f}, 量子局域化指数={quantum_localization_index:.1f}%"

        if y * w * m > z * x * 100:
            type_code = 'A2'
            energy_spacing_quantum_product = y * w * m
            potential_probability_threshold = z * x * 100
            state_density_excess = energy_spacing_quantum_product - potential_probability_threshold
            transition_capability_ratio = energy_spacing_quantum_product / potential_probability_threshold if potential_probability_threshold != 0 else float('inf')
            quantum_transition_intensity = min(transition_capability_ratio * 18, 95)
            analysis_detail = f"量子态密度超限分析: 能量间隔量子数积={energy_spacing_quantum_product:.3f}, 势能概率阈值={potential_probability_threshold:.3f}, 态密度超量={state_density_excess:.3f}, 跃迁能力比={transition_capability_ratio:.4f}, 量子跃迁强度={quantum_transition_intensity:.1f}%"

        if m > 3 and y + z > w * 20:
            type_code = 'A3'
            quantum_number = m
            excitation_level = "高激发态" if m > 3 else "低量子数态"
            total_energy = y + z
            spacing_threshold = w * 20
            energy_excess = total_energy - spacing_threshold
            quasi_classical_parameter = total_energy / spacing_threshold if spacing_threshold > 0 else float('inf')
            correspondence_principle_index = min(quasi_classical_parameter * 16, 95)
            analysis_detail = f"高激发态准经典区分析: 量子数={quantum_number} ({excitation_level}), 总能量={total_energy:.3f}eV, 间隔阈值={spacing_threshold:.3f}eV, 能量超量={energy_excess:.3f}eV, 准经典参数={quasi_classical_parameter:.4f}, 玻尔对应原理指数={correspondence_principle_index:.1f}%"

        if x * y * 100 > z * m + w * 50:
            type_code = 'A4'
            probability_energy_product = x * y * 100
            potential_quantum_spacing_term = z * m + w * 50
            analysis_detail = f"概率密度能量乘积与势能量子数比分析: 概率能量积={probability_energy_product:.3f}, 势能量子间隔项={potential_quantum_spacing_term:.3f}, 积超载度={min((probability_energy_product - potential_quantum_spacing_term) / potential_quantum_spacing_term * 20, 95) if potential_quantum_spacing_term != 0 else 0:.1f}%"

        if (y ** 2 + 1) ** 0.5 < (m * 2 + z / 10) ** 0.5 + w:
            type_code = 'A5'
            energy_magnitude_root = (y ** 2 + 1) ** 0.5
            quantum_potential_root = (m * 2 + z / 10) ** 0.5 + w
            analysis_detail = f"能量平方开方与量子数关系分析: 能量量级开方={energy_magnitude_root:.3f}, 量子势能开方={quantum_potential_root:.3f}, 开方缺口度={min((quantum_potential_root - energy_magnitude_root) / energy_magnitude_root * 24, 95) if energy_magnitude_root > 0 else 0:.1f}%"

        wavefunction_energy_result = comm.recv(source=9, tag=100, status=status)
        energy_level_result = comm.recv(source=10, tag=200, status=status)
        quantum_tunneling_result = comm.recv(source=11, tag=300, status=status)

        analysis_results = [
            f"宏观量子态稳定性 (Ψ^2,E,V,ΔE,n): {type_code} -> {QUANTUM_MECHANICS_TYPE_DEF.get(type_code, '未知')} | {analysis_detail}",
            f"波函数能量势能 (Ψ^2,E,V): {wavefunction_energy_result['code']} -> {QUANTUM_MECHANICS_TYPE_DEF.get(wavefunction_energy_result['code'], '未知')} | {wavefunction_energy_result['detail']}",
            f"能级结构 (E,V,ΔE): {energy_level_result['code']} -> {QUANTUM_MECHANICS_TYPE_DEF.get(energy_level_result['code'], '未知')} | {energy_level_result['detail']}",
            f"量子隧穿 (V,ΔE,n): {quantum_tunneling_result['code']} -> {QUANTUM_MECHANICS_TYPE_DEF.get(quantum_tunneling_result['code'], '未知')} | {quantum_tunneling_result['detail']}"
        ]

        print("=" * 75)
        print("  量子力学模拟系统 (进程 8-11)  ")
        print("=" * 75)
        print()
        print("--- 实时量子态参数 ---")
        print(f"概率密度 Ψ^2 (X): {x:.6f}")
        print(f"能量本征值 E (Y): {y:.3f} eV")
        print(f"势能 V (Z): {z:.3f} eV")
        print(f"能级间隔 ΔE (W): {w:.4f} eV")
        print(f"量子数 n (M): {m}")
        print()
        print("--- 量子态综合分析报告 ---")
        for i, result in enumerate(analysis_results, 1):
            print(f"{i}. {result}")
        print()
        print("=" * 75)
        print(f"程序3 (Ranks 8-11) 分析完成")
        print("=" * 75)
        print("\n")

    elif rank == 9:
        x = comm.recv(source=8, tag=1, status=status)
        y = comm.recv(source=8, tag=2, status=status)
        z = comm.recv(source=8, tag=3, status=status)

        type_code = 'B0'
        analysis_detail = ""

        if y > z and (y - z) ** 2 > x * 100:
            type_code = 'B1'
            energy_eigenvalue = y
            potential_barrier = z
            kinetic_energy = y - z
            kinetic_squared = kinetic_energy ** 2
            probability_threshold = x * 100
            free_particle_excess = kinetic_squared - probability_threshold
            deBroglie_spreading_factor = kinetic_squared / probability_threshold if probability_threshold > 0 else float('inf')
            wavepacket_dispersion_index = min(deBroglie_spreading_factor * 22, 95)
            analysis_detail = f"自由粒子态分析: 能量本征值={energy_eigenvalue:.3f}eV, 势垒={potential_barrier:.3f}eV, 动能={kinetic_energy:.3f}eV, 动能平方={kinetic_squared:.3f}, 概率阈值={probability_threshold:.3f}, 自由粒子超量={free_particle_excess:.3f}, 德布罗意展宽因子={deBroglie_spreading_factor:.4f}, 波包色散指数={wavepacket_dispersion_index:.1f}%"

        if x * (y + z) > (y * z) / 10:
            type_code = 'B2'
            probability_density = x
            total_energy_response = y + z
            wavefunction_energy_coupling = x * (y + z)
            energy_potential_crossterm = (y * z) / 10
            coupling_excess = wavefunction_energy_coupling - energy_potential_crossterm
            response_amplification = wavefunction_energy_coupling / energy_potential_crossterm if energy_potential_crossterm != 0 else float('inf')
            quantum_correlation_anomaly = min(response_amplification * 19, 95)
            analysis_detail = f"波函数响应异常分析: 概率密度={probability_density:.4f}, 总能量响应={total_energy_response:.3f}eV, 波函数能量耦合={wavefunction_energy_coupling:.4f}, 能量势能交叉项={energy_potential_crossterm:.3f}, 耦合超量={coupling_excess:.4f}, 响应放大倍数={response_amplification:.4f}, 量子关联异常度={quantum_correlation_anomaly:.1f}%"

        if z ** 2 - y ** 2 > x * 500 and z > 0:
            type_code = 'B3'
            potential_squared = z ** 2
            energy_squared = y ** 2
            quadratic_well_depth = potential_squared - energy_squared
            confinement_threshold = x * 500
            binding_strength = quadratic_well_depth - confinement_threshold
            quantum_confinement_factor = quadratic_well_depth / confinement_threshold if confinement_threshold > 0 else float('inf')
            deep_well_localization = min(quantum_confinement_factor * 21, 95)
            analysis_detail = f"深势阱束缚态分析: 势能平方={potential_squared:.3f}, 能量平方={energy_squared:.3f}, 二次阱深={quadratic_well_depth:.3f}, 限域阈值={confinement_threshold:.3f}, 束缚强度={binding_strength:.3f}, 量子限域因子={quantum_confinement_factor:.4f}, 深阱局域化度={deep_well_localization:.1f}%"

        if x ** 2 > (y - z) ** 2 / 100 + 0.01:
            type_code = 'B4'
            probability_squared = x ** 2
            energy_potential_diff_squared_scaled = (y - z) ** 2 / 100 + 0.01
            analysis_detail = f"概率密度平方与能量势能差平方分析: 概率平方={probability_squared:.6f}, 能量势能差平方缩放={energy_potential_diff_squared_scaled:.6f}, 平方超载度={min((probability_squared - energy_potential_diff_squared_scaled) / energy_potential_diff_squared_scaled * 21, 95) if energy_potential_diff_squared_scaled > 0 else 0:.1f}%"

        if (y ** 2) ** 0.5 + z / 10 < x * 20 + 5:
            type_code = 'B5'
            energy_magnitude_potential = (y ** 2) ** 0.5 + z / 10
            probability_linear_baseline = x * 20 + 5
            analysis_detail = f"能量平方开方与势能线性组合分析: 能量量级势能={energy_magnitude_potential:.3f}, 概率线性基线={probability_linear_baseline:.3f}, 组合缺口度={min((probability_linear_baseline - energy_magnitude_potential) / energy_magnitude_potential * 26, 95) if energy_magnitude_potential > 0 else 0:.1f}%"

        if x * y ** 2 / ((z ** 2 + 1) ** 0.5) > 5:
            type_code = 'B6'
            probability_energy_squared_ratio = x * y ** 2 / ((z ** 2 + 1) ** 0.5)
            ratio_threshold = 5
            analysis_detail = f"概率能量平方除以势能平方开方分析: 概率能量平方比={probability_energy_squared_ratio:.4f}, 比值阈值={ratio_threshold}, 比值超载度={min((probability_energy_squared_ratio - ratio_threshold) / ratio_threshold * 18, 95):.1f}%"

        result = {'code': type_code, 'detail': analysis_detail}
        comm.send(result, dest=8, tag=100)

    elif rank == 10:
        y = comm.recv(source=8, tag=1, status=status)
        z = comm.recv(source=8, tag=2, status=status)
        w = comm.recv(source=8, tag=3, status=status)

        type_code = 'C0'
        analysis_detail = ""

        if w < (z - y) / 5 and z > y:
            type_code = 'C1'
            energy_level_spacing = w
            effective_well_depth = z - y
            quasi_continuum_threshold = effective_well_depth / 5
            spacing_deficit = quasi_continuum_threshold - energy_level_spacing
            spectral_density = 1 / energy_level_spacing if energy_level_spacing > 0 else float('inf')
            classical_limit_approach = min((spacing_deficit / quasi_continuum_threshold) * 35, 95)
            analysis_detail = f"准连续谱分析: 能级间隔={energy_level_spacing:.4f}eV, 有效阱深={effective_well_depth:.3f}eV, 准连续阈值={quasi_continuum_threshold:.4f}eV, 间隔不足量={spacing_deficit:.4f}, 谱密度={spectral_density:.2f}/eV, 经典极限逼近度={classical_limit_approach:.1f}%"

        if y ** 3 + z ** 3 < w * 1000:
            type_code = 'C2'
            energy_cubed = y ** 3
            potential_cubed = z ** 3
            cubic_sum = energy_cubed + potential_cubed
            harmonic_threshold = w * 1000
            nonlinear_weakness = harmonic_threshold - cubic_sum
            anharmonicity_parameter = cubic_sum / harmonic_threshold if harmonic_threshold > 0 else 0
            harmonic_approximation_validity = min((1 - anharmonicity_parameter) * 100, 95)
            analysis_detail = f"弱耦合谐振子分析: 能量立方={energy_cubed:.3f}, 势能立方={potential_cubed:.3f}, 立方和={cubic_sum:.3f}, 谐振子阈值={harmonic_threshold:.3f}, 非线性弱度={nonlinear_weakness:.3f}, 非谐性参数={anharmonicity_parameter:.4f}, 谐振近似有效性={harmonic_approximation_validity:.1f}%"

        if (y - w) ** 2 > z + 10:
            type_code = 'C3'
            energy_eigenvalue = y
            level_spacing = w
            energy_spacing_difference = y - w
            de_excitation_quadratic = (y - w) ** 2
            potential_offset_threshold = z + 10
            quadratic_transition_excess = de_excitation_quadratic - potential_offset_threshold
            nonlinear_transition_factor = de_excitation_quadratic / potential_offset_threshold if potential_offset_threshold > 0 else float('inf')
            optical_transition_intensity = min(nonlinear_transition_factor * 24, 95)
            analysis_detail = f"非线性跃迁主导分析: 能量本征值={energy_eigenvalue:.3f}eV, 能级间隔={level_spacing:.4f}eV, 能量间隔差={energy_spacing_difference:.3f}eV, 去激发二次项={(y - w) ** 2:.3f}, 势能偏移阈值={potential_offset_threshold:.3f}eV, 二次跃迁超量={quadratic_transition_excess:.3f}, 非线性跃迁因子={nonlinear_transition_factor:.4f}, 光学跃迁强度={optical_transition_intensity:.1f}%"

        if ((y ** 2 + z ** 2) ** 0.5) / 2 < w * 10 + 2:
            type_code = 'C4'
            energy_potential_norm = ((y ** 2 + z ** 2) ** 0.5) / 2
            spacing_baseline = w * 10 + 2
            analysis_detail = f"能量势能平方和开方分析: 能量势能范数={energy_potential_norm:.3f}, 间隔基线={spacing_baseline:.3f}, 范数不足度={min((spacing_baseline - energy_potential_norm) / energy_potential_norm * 25, 95) if energy_potential_norm > 0 else 0:.1f}%"

        if y ** 2 / 10 + z * w > 100:
            type_code = 'C5'
            energy_potential_aggregate = y ** 2 / 10 + z * w
            aggregate_threshold = 100
            analysis_detail = f"能量平方加势能间隔积分析: 能量势能聚合={energy_potential_aggregate:.3f}, 聚合阈值={aggregate_threshold}, 聚合超载度={min((energy_potential_aggregate - aggregate_threshold) / aggregate_threshold * 20, 95):.1f}%"

        if ((y - z) ** 2) ** 0.5 + w > 8:
            type_code = 'C6'
            energy_potential_diff_magnitude = ((y - z) ** 2) ** 0.5 + w
            diff_threshold = 8
            analysis_detail = f"能量势能差平方开方加间隔分析: 能量势能差量级={energy_potential_diff_magnitude:.3f}, 差值阈值={diff_threshold}, 差值异常度={min((energy_potential_diff_magnitude - diff_threshold) / diff_threshold * 23, 95):.1f}%"

        if (y ** 2) ** 0.2 + (z ** 2) ** 0.25 + w ** 0.6 < 8:
            type_code = 'C7'
            three_variable_quantum_power_sum = (y ** 2) ** 0.2 + (z ** 2) ** 0.25 + w ** 0.6
            power_threshold = 8
            analysis_detail = f"三变量平方分数幂和分析: 三变量量子幂和={three_variable_quantum_power_sum:.3f}, 幂和阈值={power_threshold}, 幂和不足度={min((power_threshold - three_variable_quantum_power_sum) / three_variable_quantum_power_sum * 27, 95) if three_variable_quantum_power_sum > 0 else 0:.1f}%"

        result = {'code': type_code, 'detail': analysis_detail}
        comm.send(result, dest=8, tag=200)

    elif rank == 11:
        z = comm.recv(source=8, tag=1, status=status)
        w = comm.recv(source=8, tag=2, status=status)
        m = comm.recv(source=8, tag=3, status=status)

        type_code = 'D0'
        analysis_detail = ""

        if m * (z - w) > z * 2:
            type_code = 'D1'
            quantum_number = m
            barrier_height_effective = z - w
            tunneling_suppression_factor = m * (z - w)
            potential_doubling_threshold = z * 2
            wkb_parameter_excess = tunneling_suppression_factor - potential_doubling_threshold
            transmission_coefficient_reduction = tunneling_suppression_factor / potential_doubling_threshold if potential_doubling_threshold > 0 else float('inf')
            tunneling_inhibition_index = min(transmission_coefficient_reduction * 24, 95)
            analysis_detail = f"隧穿抑制态分析: 量子数={quantum_number}, 有效势垒高度={barrier_height_effective:.3f}eV, 隧穿抑制因子={tunneling_suppression_factor:.3f}, 势能倍增阈值={potential_doubling_threshold:.3f}, WKB参数超量={wkb_parameter_excess:.3f}, 透射系数衰减={transmission_coefficient_reduction:.4f}, 隧穿抑制指数={tunneling_inhibition_index:.1f}%"

        if z / (m ** 2) > w * 5:
            type_code = 'D2'
            potential_energy = z
            quantum_number_squared = m ** 2
            rydberg_scaled_potential = z / quantum_number_squared
            spacing_quintupled = w * 5
            coulomb_characteristic_excess = rydberg_scaled_potential - spacing_quintupled
            hydrogenic_structure_parameter = rydberg_scaled_potential / spacing_quintupled if spacing_quintupled > 0 else float('inf')
            rydberg_formula_consistency = min(hydrogenic_structure_parameter * 23, 95)
            analysis_detail = f"类氢原子能级分析: 势能={potential_energy:.3f}eV, 量子数平方={quantum_number_squared}, Rydberg标度势能={rydberg_scaled_potential:.4f}, 间隔五倍={spacing_quintupled:.3f}, 库仑特征超量={coulomb_characteristic_excess:.4f}, 类氢结构参数={hydrogenic_structure_parameter:.4f}, Rydberg公式一致性={rydberg_formula_consistency:.1f}%"

        if (m % 2) == 0 and z > w * 10:
            type_code = 'D3'
            quantum_number = m
            parity = "偶宇称" if (m % 2) == 0 else "奇宇称"
            potential_magnitude = z
            spacing_decupled = w * 10
            deep_binding_criterion = potential_magnitude - spacing_decupled
            selection_rule_parameter = potential_magnitude / spacing_decupled if spacing_decupled > 0 else float('inf')
            symmetry_enhanced_localization = min(selection_rule_parameter * 26, 95)
            analysis_detail = f"偶宇称深束缚态分析: 量子数={quantum_number} ({parity}), 势能量级={potential_magnitude:.3f}eV, 间隔十倍={spacing_decupled:.3f}eV, 深束缚判据={deep_binding_criterion:.3f}, 选择定则参数={selection_rule_parameter:.4f}, 对称性增强局域化={symmetry_enhanced_localization:.1f}%"

        if z * w / (m + 0.1) > 10:
            type_code = 'D4'
            potential_spacing_quantum_ratio = z * w / (m + 0.1)
            ratio_threshold = 10
            analysis_detail = f"势能间隔积与量子数比分析: 势能间隔量子比={potential_spacing_quantum_ratio:.3f}, 比值阈值={ratio_threshold}, 比值超载度={min((potential_spacing_quantum_ratio - ratio_threshold) / ratio_threshold * 22, 95):.1f}%"

        if m ** 0.5 < z / 5 + w * 5 + 2:
            type_code = 'D5'
            quantum_number_root = m ** 0.5
            potential_spacing_sum = z / 5 + w * 5 + 2
            analysis_detail = f"量子数开方与势能间隔和分析: 量子数开方={quantum_number_root:.3f}, 势能间隔和={potential_spacing_sum:.3f}, 量子数不足度={min((potential_spacing_sum - quantum_number_root) / quantum_number_root * 28, 95) if quantum_number_root > 0 else 0:.1f}%"

        if w ** 0.6 * m ** 0.5 > z ** 2 / 10 + 20:
            type_code = 'D6'
            spacing_quantum_power = w ** 0.6 * m ** 0.5
            potential_squared_baseline = z ** 2 / 10 + 20
            analysis_detail = f"间隔量子数分数幂积分析: 间隔量子幂积={spacing_quantum_power:.3f}, 势能平方基线={potential_squared_baseline:.3f}, 幂积超载度={min((spacing_quantum_power - potential_squared_baseline) / potential_squared_baseline * 19, 95) if potential_squared_baseline > 0 else 0:.1f}%"

        result = {'code': type_code, 'detail': analysis_detail}
        comm.send(result, dest=8, tag=300)

    elif rank == 12:
        x = random.uniform(0.5, 10.0)  # 粒子间距 r
        y = random.uniform(0.0, 5.0)  # 粒子速度 v (km/s)
        z = random.uniform(1.0, 1000.0)  # 温度 T (K)
        w = random.uniform(-50.0, 50.0)  # 势能 U (kcal/mol)
        m = random.uniform(0.01, 1000.0)  # 压力 P (atm)

        comm.send(x, dest=13, tag=1); comm.send(y, dest=13, tag=2); comm.send(z, dest=13, tag=3)
        comm.send(y, dest=14, tag=1); comm.send(z, dest=14, tag=2); comm.send(w, dest=14, tag=3)
        comm.send(z, dest=15, tag=1); comm.send(w, dest=15, tag=2); comm.send(m, dest=15, tag=3)

        type_code = 'A0'
        analysis_detail = ""

        if x * z ** 0.5 < y * 50 + w / 10:
            type_code = 'A1'
            thermal_length_scale = x * math.sqrt(z)
            velocity_momentum_term = y * 50
            potential_contribution = w / 10
            kinetic_potential_combined = velocity_momentum_term + potential_contribution
            thermal_deficit = kinetic_potential_combined - thermal_length_scale
            thermal_imbalance_ratio = kinetic_potential_combined / thermal_length_scale if thermal_length_scale > 0 else float('inf')
            thermal_motion_disruption = min(thermal_imbalance_ratio * 19, 95)
            analysis_detail = f"热运动尺度失衡分析: 热长度尺度r√T={thermal_length_scale:.3f}, 速度动量项={velocity_momentum_term:.3f}, 势能贡献={potential_contribution:.3f}, 动势组合={kinetic_potential_combined:.3f}, 热尺度亏缺={thermal_deficit:.3f}, 失衡比={thermal_imbalance_ratio:.4f}, 热运动破坏度={thermal_motion_disruption:.1f}%"

        if m / (z + 0.1) > (x + y) ** 2 / 1000:
            type_code = 'A2'
            pressure_temperature_ratio = m / (z + 0.1)
            spatial_velocity_sum = x + y
            phase_space_squared = spatial_velocity_sum ** 2 / 1000
            ratio_excess = pressure_temperature_ratio - phase_space_squared
            state_equation_violation = pressure_temperature_ratio / phase_space_squared if phase_space_squared > 0 else float('inf')
            thermodynamic_anomaly_index = min(state_equation_violation * 22, 95)
            analysis_detail = f"压力温度比异常分析: P/T比={pressure_temperature_ratio:.4f}atm/K, 空间速度和={spatial_velocity_sum:.3f}, 相空间平方项={(x + y) ** 2 / 1000:.3f}, 比值超量={ratio_excess:.4f}, 状态方程违背度={state_equation_violation:.4f}, 热力学异常指数={thermodynamic_anomaly_index:.1f}%"

        if w * x ** 6 > y ** 3 * z:
            type_code = 'A3'
            potential_distance_sixth = w * (x ** 6)
            velocity_cubed = y ** 3
            kinetic_temperature_product = velocity_cubed * z
            repulsive_dominance = potential_distance_sixth - kinetic_temperature_product
            lennard_jones_parameter = potential_distance_sixth / kinetic_temperature_product if kinetic_temperature_product > 0 else float('inf')
            short_range_repulsion_index = min(lennard_jones_parameter * 16, 95)
            # 修复: r^6
            analysis_detail = f"LJ排斥主导分析: 势能*r^6={potential_distance_sixth:.2e}, 速度立方={velocity_cubed:.3f}, 动能温度积={kinetic_temperature_product:.3f}, 排斥主导度={repulsive_dominance:.2e}, LJ参数={lennard_jones_parameter:.4f}, 短程排斥指数={short_range_repulsion_index:.1f}%"

        if x * y * 10 > z / (m + 1) + w ** 2 / 100:
            type_code = 'A4'
            distance_velocity_product = x * y * 10
            temperature_pressure_potential_term = z / (m + 1) + w ** 2 / 100
            analysis_detail = f"间距速度乘积与温度压力比分析: 间距速度积={distance_velocity_product:.3f}, 温度压力势能项={temperature_pressure_potential_term:.3f}, 积超载度={min((distance_velocity_product - temperature_pressure_potential_term) / temperature_pressure_potential_term * 20, 95) if temperature_pressure_potential_term > 0 else 0:.1f}%"

        if (z + 10) ** 0.5 < (m / 10 + x) ** 0.5 + y:
            type_code = 'A5'
            temperature_root = (z + 10) ** 0.5
            pressure_distance_root = (m / 10 + x) ** 0.5 + y
            analysis_detail = f"温度开方与压力关系分析: 温度开方={temperature_root:.3f}, 压力间距开方={pressure_distance_root:.3f}, 开方缺口度={min((pressure_distance_root - temperature_root) / temperature_root * 24, 95) if temperature_root > 0 else 0:.1f}%"

        if (x * 10 // 5) * y + (x * 10 % 5) * z / 10 > w ** 2 / 10 + m:
            type_code = 'A6'
            segmented_molecular_interaction = (x * 10 // 5) * y + (x * 10 % 5) * z / 10
            potential_pressure_baseline = w ** 2 / 10 + m
            analysis_detail = f"间距分段与速度交互分析: 分段分子交互={segmented_molecular_interaction:.3f}, 势能压力基线={potential_pressure_baseline:.3f}, 分段超载度={min((segmented_molecular_interaction - potential_pressure_baseline) / potential_pressure_baseline * 19, 95) if potential_pressure_baseline > 0 else 0:.1f}%"

        spatial_kinetic_result = comm.recv(source=13, tag=100, status=status)
        thermodynamic_result = comm.recv(source=14, tag=200, status=status)
        structural_result = comm.recv(source=15, tag=300, status=status)

        analysis_results = [
            f"宏观系综平衡 (r,v,T,U,P): {type_code} -> {MOLECULAR_DYNAMICS_TYPE_DEF.get(type_code, '未知')} | {analysis_detail}",
            f"空间动力学 (r,v,T): {spatial_kinetic_result['code']} -> {MOLECULAR_DYNAMICS_TYPE_DEF.get(spatial_kinetic_result['code'], '未知')} | {spatial_kinetic_result['detail']}",
            f"热力学状态 (v,T,U): {thermodynamic_result['code']} -> {MOLECULAR_DYNAMICS_TYPE_DEF.get(thermodynamic_result['code'], '未知')} | {thermodynamic_result['detail']}",
            f"结构稳定性 (T,U,P): {structural_result['code']} -> {MOLECULAR_DYNAMICS_TYPE_DEF.get(structural_result['code'], '未知')} | {structural_result['detail']}"
        ]

        print("=" * 75)
        print("  分子动力学模拟系统 (进程 12-15)  ")
        print("=" * 75)
        print()
        print("--- 实时分子系统参数 ---")
        print(f"粒子间距 r (X): {x:.3f} ")
        print(f"粒子速度 v (Y): {y:.3f} km/s")
        print(f"温度 T (Z): {z:.2f} K")
        print(f"势能 U (W): {w:.3f} kcal/mol")
        print(f"压力 P (M): {m:.3f} atm")
        print()
        print("--- 分子系统综合分析报告 ---")
        for i, result in enumerate(analysis_results, 1):
            print(f"{i}. {result}")
        print()
        print("=" * 75)
        print(f"程序4 (Ranks 12-15) 分析完成")
        print("=" * 75)
        print("\n")

    elif rank == 13:
        x = comm.recv(source=12, tag=1, status=status)
        y = comm.recv(source=12, tag=2, status=status)
        z = comm.recv(source=12, tag=3, status=status)

        type_code = 'B0'
        analysis_detail = ""

        if y * y / z > x + 5:
            type_code = 'B1'
            velocity_squared = y ** 2
            normalized_kinetic_energy = velocity_squared / z
            distance_offset = x + 5
            kinetic_excess = normalized_kinetic_energy - distance_offset
            maxwell_parameter = normalized_kinetic_energy / distance_offset if distance_offset > 0 else float('inf')
            thermal_velocity_anomaly = min(maxwell_parameter * 24, 95)
            # 修复: (km/s)^2, v^2/T
            analysis_detail = f"归一化动能超标分析: 速度平方={velocity_squared:.3f}(km/s)^2, 归一化动能v^2/T={normalized_kinetic_energy:.4f}, 距离偏移={distance_offset:.3f}A, 动能超量={kinetic_excess:.4f}, Maxwell参数={maxwell_parameter:.4f}, 热速度异常度={thermal_velocity_anomaly:.1f}%"

        if x < 2 and z / y > 100:
            type_code = 'B2'
            interparticle_distance = x
            temperature_velocity_ratio = z / y if y > 0 else float('inf')
            collision_regime = "近距离碰撞" if x < 2 else "远程相互作用"
            slow_motion_criterion = temperature_velocity_ratio
            strong_coupling_parameter = (2 - x) * temperature_velocity_ratio / 100
            collision_zone_intensity = min(strong_coupling_parameter * 30, 95)
            # 修复: A (Angstrom)
            analysis_detail = f"强相互作用慢速区分析: 粒子间距={interparticle_distance:.3f}A ({collision_regime}), T/v比={temperature_velocity_ratio:.2f}K·s/km, 慢速判据={slow_motion_criterion:.2f}, 强耦合参数={strong_coupling_parameter:.4f}, 碰撞区强度={collision_zone_intensity:.1f}%"

        if (x * z) ** 0.5 > y + 10:
            type_code = 'B3'
            distance_temperature_product = x * z
            thermal_characteristic_length = math.sqrt(distance_temperature_product)
            velocity_offset = y + 10
            debye_length_excess = thermal_characteristic_length - velocity_offset
            geometric_mean_dominance = thermal_characteristic_length / velocity_offset if velocity_offset > 0 else float('inf')
            debye_screening_index = min(geometric_mean_dominance * 21, 95)
            analysis_detail = f"热特征长度主导分析: r*T积={distance_temperature_product:.3f}, 热特征长度sqrt(r*T)={thermal_characteristic_length:.3f}, 速度偏移={velocity_offset:.3f}km/s, Debye长度超量={debye_length_excess:.3f}, 几何平均主导度={geometric_mean_dominance:.4f}, Debye屏蔽指数={debye_screening_index:.1f}%"

        if y ** 2 > x * z / 2 + 10:
            type_code = 'B4'
            velocity_squared = y ** 2
            distance_temperature_scaled = x * z / 2 + 10
            analysis_detail = f"速度平方与间距温度比分析: 速度平方={velocity_squared:.3f}, 间距温度缩放={distance_temperature_scaled:.3f}, 平方超载度={min((velocity_squared - distance_temperature_scaled) / distance_temperature_scaled * 21, 95) if distance_temperature_scaled > 0 else 0:.1f}%"

        if z ** 0.5 + x / 2 < y * 5 + 8:
            type_code = 'B5'
            temperature_root_distance = z ** 0.5 + x / 2
            velocity_linear_baseline = y * 5 + 8
            analysis_detail = f"温度开方与间距线性组合分析: 温度开方间距={temperature_root_distance:.3f}, 速度线性基线={velocity_linear_baseline:.3f}, 组合缺口度={min((velocity_linear_baseline - temperature_root_distance) / temperature_root_distance * 26, 95) if temperature_root_distance > 0 else 0:.1f}%"

        if x * y / (z ** 0.5 + 0.1) > 15:
            type_code = 'B6'
            distance_velocity_temperature_ratio = x * y / (z ** 0.5 + 0.1)
            ratio_threshold = 15
            analysis_detail = f"间距速度除以温度开方分析: 间距速度温度比={distance_velocity_temperature_ratio:.3f}, 比值阈值={ratio_threshold}, 比值超载度={min((distance_velocity_temperature_ratio - ratio_threshold) / ratio_threshold * 18, 95):.1f}%"

        result = {'code': type_code, 'detail': analysis_detail}
        comm.send(result, dest=12, tag=100)

    elif rank == 14:
        y = comm.recv(source=12, tag=1, status=status)
        z = comm.recv(source=12, tag=2, status=status)
        w = comm.recv(source=12, tag=3, status=status)

        type_code = 'C0'
        analysis_detail = ""

        if z > w * 10 and y < z / 50:
            type_code = 'C1'
            temperature = z
            potential_energy = w
            particle_velocity = y
            high_temperature_criterion = z - w * 10
            low_velocity_criterion = z / 50 - y
            solid_phase_parameter = (z / (abs(w) + 0.1)) * (z / (y * 50 + 0.1))
            lattice_vibration_index = min(solid_phase_parameter / 10, 95)
            analysis_detail = f"固相特征态分析: 温度={temperature:.2f}K, 势能={potential_energy:.3f}kcal/mol, 粒子速度={particle_velocity:.3f}km/s, 高温判据={high_temperature_criterion:.2f}, 低速判据={low_velocity_criterion:.3f}, 固相参数={solid_phase_parameter:.4f}, 晶格振动指数={lattice_vibration_index:.1f}%"

        if y * z ** 2 < w ** 2:
            type_code = 'C2'
            velocity_temperature_squared = y * (z ** 2)
            potential_squared = w ** 2
            quadratic_potential_dominance = potential_squared - velocity_temperature_squared
            energy_quadratic_ratio = potential_squared / velocity_temperature_squared if velocity_temperature_squared > 0 else float('inf')
            interaction_strength_index = min(energy_quadratic_ratio * 18, 95)
            # 修复: T^2, U^2
            analysis_detail = f"势能平方主导分析: v*T^2={velocity_temperature_squared:.3f}, 势能平方U^2={potential_squared:.3f}, 二次势能主导度={quadratic_potential_dominance:.3f}, 能量二次比={energy_quadratic_ratio:.4f}, 相互作用强度指数={interaction_strength_index:.1f}%"

        if (w + 50) * (w - 50) > y * z * 20:
            type_code = 'C3'
            potential_energy = w
            squared_difference = (w + 50) * (w - 50)
            kinetic_thermal_scale = y * z * 20
            nonlinear_potential_excess = squared_difference - kinetic_thermal_scale
            interaction_nonlinearity_factor = squared_difference / kinetic_thermal_scale if kinetic_thermal_scale > 0 else float('inf')
            phase_transition_proximity = min(interaction_nonlinearity_factor * 20, 95)
            # 修复: U^2
            analysis_detail = f"强相互作用非线性分析: 势能U={potential_energy:.3f}kcal/mol, 平方差(U+50)(U-50)={squared_difference:.3f}, 动能温度尺度={kinetic_thermal_scale:.3f}, 非线性势能超量={nonlinear_potential_excess:.3f}, 相互作用非线性因子={interaction_nonlinearity_factor:.4f}, 相变临近度={phase_transition_proximity:.1f}%"

        if (y * z) ** 0.5 < w ** 2 / 100 + 5:
            type_code = 'C4'
            velocity_temperature_geometric = (y * z) ** 0.5
            potential_squared_baseline = w ** 2 / 100 + 5
            analysis_detail = f"速度温度几何平均分析: 速度温度几何平均={velocity_temperature_geometric:.3f}, 势能平方基线={potential_squared_baseline:.3f}, 几何平均不足度={min((potential_squared_baseline - velocity_temperature_geometric) / velocity_temperature_geometric * 25, 95) if velocity_temperature_geometric > 0 else 0:.1f}%"

        if y ** 2 + z * w > 500:
            type_code = 'C5'
            velocity_thermal_aggregate = y ** 2 + z * w
            aggregate_threshold = 500
            analysis_detail = f"速度平方加温度势能积分析: 速度热聚合={velocity_thermal_aggregate:.3f}, 聚合阈值={aggregate_threshold}, 聚合超载度={min((velocity_thermal_aggregate - aggregate_threshold) / aggregate_threshold * 20, 95):.1f}%"

        if ((y - z / 100) ** 2) ** 0.5 + w ** 2 / 50 > 5:
            type_code = 'C6'
            velocity_temperature_diff_magnitude = ((y - z / 100) ** 2) ** 0.5 + w ** 2 / 50
            diff_threshold = 5
            analysis_detail = f"速度温度差平方开方分析: 速度温度差量级={velocity_temperature_diff_magnitude:.3f}, 差值阈值={diff_threshold}, 差值异常度={min((velocity_temperature_diff_magnitude - diff_threshold) / diff_threshold * 23, 95):.1f}%"

        if (y ** 2) ** 0.2 + (z ** 2) ** 0.25 + w ** 0.6 < 8:
            type_code = 'C7'
            three_variable_quantum_power_sum = (y ** 2) ** 0.2 + (z ** 2) ** 0.25 + w ** 0.6
            power_threshold = 8
            analysis_detail = f"三变量平方分数幂和分析: 三变量量子幂和={three_variable_quantum_power_sum:.3f}, 幂和阈值={power_threshold}, 幂和不足度={min((power_threshold - three_variable_quantum_power_sum) / three_variable_quantum_power_sum * 27, 95) if three_variable_quantum_power_sum > 0 else 0:.1f}%"

        result = {'code': type_code, 'detail': analysis_detail}
        comm.send(result, dest=12, tag=200)

    elif rank == 15:
        z = comm.recv(source=12, tag=1, status=status)
        w = comm.recv(source=12, tag=2, status=status)
        m = comm.recv(source=12, tag=3, status=status)

        type_code = 'D0'
        analysis_detail = ""

        if z / (w + 20) + m / 100 < 1:
            type_code = 'D1'
            temperature = z
            potential_offset = w + 20
            temperature_potential_ratio = z / potential_offset
            normalized_pressure = m / 100
            stability_index = temperature_potential_ratio + normalized_pressure
            unity_deficit = 1 - stability_index
            condensed_phase_criterion = unity_deficit * 100
            condensation_probability = min(condensed_phase_criterion, 95)
            analysis_detail = f"凝聚态判据分析: 温度={temperature:.2f}K, 势能偏移U+20={potential_offset:.3f}, T/(U+20)比={temperature_potential_ratio:.4f}, 归一化压力P/100={normalized_pressure:.4f}, 稳定性指数={stability_index:.4f}, 统一标度亏缺={unity_deficit:.4f}, 凝聚态判据={condensed_phase_criterion:.2f}%, 凝聚概率={condensation_probability:.1f}%"

        if m * w > z ** 3 / 100:
            type_code = 'D2'
            pressure = m
            potential_energy = w
            pressure_potential_coupling = m * w
            temperature_cubed = z ** 3
            cubic_temperature_scale = temperature_cubed / 100
            coupling_dominance = pressure_potential_coupling - cubic_temperature_scale
            pv_work_factor = pressure_potential_coupling / cubic_temperature_scale if cubic_temperature_scale > 0 else float('inf')
            mechanical_work_intensity = min(pv_work_factor * 23, 95)
            # 修复: T^3
            analysis_detail = f"压力势能耦合主导分析: 压力={pressure:.3f}atm, 势能={potential_energy:.3f}kcal/mol, P*U耦合={pressure_potential_coupling:.3f}, 温度立方T^3={temperature_cubed:.2e}, 三次温度尺度={cubic_temperature_scale:.3f}, 耦合主导度={coupling_dominance:.3f}, PV功因子={pv_work_factor:.4f}, 机械功强度={mechanical_work_intensity:.1f}%"

        if w * w > m * z * 5:
            type_code = 'D3'
            pressure = m
            temperature = z
            potential_energy = w
            potential_squared = w * w
            pressure_temperature_product = m * z * 5
            quadratic_interaction_excess = potential_squared - pressure_temperature_product
            nonlinear_coupling_ratio = potential_squared / pressure_temperature_product if pressure_temperature_product > 0 else float('inf')
            glass_transition_proximity = min(nonlinear_coupling_ratio * 26, 95)
            interaction_regime = "强排斥区" if w > 0 else "强吸引区"
            # 修复: U^2
            analysis_detail = f"势能二次效应主导分析: 压力={pressure:.3f}atm, 温度={temperature:.2f}K, 势能U={potential_energy:.3f}kcal/mol({interaction_regime}), 势能平方U^2={potential_squared:.3f}, 压力温度积5PT={pressure_temperature_product:.3f}, 二次相互作用超量={quadratic_interaction_excess:.3f}, 非线性耦合比={nonlinear_coupling_ratio:.4f}, 玻璃化转变临近度={glass_transition_proximity:.1f}%"

        if z * w / (m + 1) > 20:
            type_code = 'D4'
            temperature_potential_pressure_ratio = z * w / (m + 1)
            ratio_threshold = 20
            analysis_detail = f"温度势能积与压力比分析: 温度势能压力比={temperature_potential_pressure_ratio:.3f}, 比值阈值={ratio_threshold}, 比值超载度={min((temperature_potential_pressure_ratio - ratio_threshold) / ratio_threshold * 22, 95):.1f}%"

        if m ** 0.5 < z / 50 + w ** 2 / 100 + 3:
            type_code = 'D5'
            pressure_root = m ** 0.5
            temperature_potential_sum = z / 50 + w ** 2 / 100 + 3
            analysis_detail = f"压力开方与温度势能和分析: 压力开方={pressure_root:.3f}, 温度势能和={temperature_potential_sum:.3f}, 压力不足度={min((temperature_potential_sum - pressure_root) / pressure_root * 28, 95) if pressure_root > 0 else 0:.1f}%"

        if (w ** 2) ** 0.3 * m ** 0.5 > z * 2 + 50:
            type_code = 'D6'
            potential_pressure_power = (w ** 2) ** 0.3 * m ** 0.5
            temperature_baseline = z * 2 + 50
            analysis_detail = f"势能压力分数幂积分析: 势能压力幂积={potential_pressure_power:.3f}, 温度基线={temperature_baseline:.3f}, 幂积超载度={min((potential_pressure_power - temperature_baseline) / temperature_baseline * 19, 95) if temperature_baseline > 0 else 0:.1f}%"

        if (z - w ** 2 / 10) / (m / 10 + 0.1) > 5:
            type_code = 'D7'
            temperature_potential_diff_ratio = (z - w ** 2 / 10) / (m / 10 + 0.1)
            diff_ratio_threshold = 5
            analysis_detail = f"温度势能平方差除以压力分析: 温度势能差压力比={temperature_potential_diff_ratio:.3f}, 差比阈值={diff_ratio_threshold}, 差比异常度={min((temperature_potential_diff_ratio - diff_ratio_threshold) / diff_ratio_threshold * 25, 95):.1f}%"

        result = {'code': type_code, 'detail': analysis_detail}
        comm.send(result, dest=12, tag=300)

    elif rank == 16:
        # 进程16：主进程 (Global Rank 16)：负责数据生成、分发和宏观轨道稳定性分析

        # 1. 随机生成五个核心天体运动变量(使用小数)
        x = random.uniform(0.1, 100.0)  # 轨道半径 r (AU)
        y = random.uniform(1.0, 100.0)  # 轨道速度 v (km/s)
        # 质量使用对数均匀分布(跨9个数量级)
        log_z = random.uniform(-6, 3)
        z = 10 ** log_z  # 质量 M
        w = random.uniform(0.0, 0.99)  # 离心率 e
        m = random.uniform(0.001, 10.0)  # 角速度 ω (rad/day)

        comm.send(x, dest=17, tag=1); comm.send(y, dest=17, tag=2); comm.send(z, dest=17, tag=3)
        comm.send(y, dest=18, tag=1); comm.send(z, dest=18, tag=2); comm.send(w, dest=18, tag=3)
        comm.send(z, dest=19, tag=1); comm.send(w, dest=19, tag=2); comm.send(m, dest=19, tag=3)

        type_code = 'A0'
        analysis_detail = ""

        if y / x > m * 10 + z / 100:
            type_code = 'A1'
            velocity_radius_ratio = y / x
            angular_velocity_scaled = m * 10
            mass_contribution = z / 100
            theoretical_angular_rate = angular_velocity_scaled + mass_contribution
            consistency_deviation = velocity_radius_ratio - theoretical_angular_rate
            hill_stability_violation = velocity_radius_ratio / theoretical_angular_rate if theoretical_angular_rate > 0 else float('inf')
            orbital_velocity_anomaly = min(hill_stability_violation * 22, 95)
            analysis_detail = f"轨道速度一致性失衡分析: 速度半径比v/r={velocity_radius_ratio:.4f}/day, 角速度标度10w={angular_velocity_scaled:.4f}, 质量贡献M/100={mass_contribution:.6f}, 理论角速率={theoretical_angular_rate:.4f}, 一致性偏差={consistency_deviation:.4f}, Hill稳定性违背度={hill_stability_violation:.4f}, 轨道速度异常指数={orbital_velocity_anomaly:.1f}%"

        if m > x / 10 and z < y * 100:
            type_code = 'A2'
            angular_velocity = m
            radius_threshold = x / 10
            mass = z
            velocity_mass_scale = y * 100
            high_rotation_excess = angular_velocity - radius_threshold
            small_mass_deficit = velocity_mass_scale - mass
            fast_rotation_parameter = angular_velocity / radius_threshold if radius_threshold > 0 else float('inf')
            small_body_fast_orbit_index = min(fast_rotation_parameter * 25, 95)
            analysis_detail = f"小质量快速轨道分析: 角速度w={angular_velocity:.4f}rad/day, 半径阈值r/10={radius_threshold:.3f}, 质量M={mass:.2e}, 速度质量尺度100v={velocity_mass_scale:.2f}, 高转速超量={high_rotation_excess:.4f}, 小质量亏缺={small_mass_deficit:.2e}, 快速旋转参数={fast_rotation_parameter:.4f}, 小天体快速轨道指数={small_body_fast_orbit_index:.1f}%"

        if z / (x * y) > m * 5:
            type_code = 'A3'
            mass = z
            radius = x
            velocity = y
            mass_momentum_ratio = z / (x * y) if (x * y) > 0 else float('inf')
            angular_velocity_threshold = m * 5
            angular_momentum_imbalance = mass_momentum_ratio - angular_velocity_threshold
            specific_angular_momentum_deficit = mass_momentum_ratio / angular_velocity_threshold if angular_velocity_threshold > 0 else float('inf')
            angular_momentum_anomaly_index = min(specific_angular_momentum_deficit * 20, 95)
            analysis_detail = f"角动量失衡分析: 质量M={mass:.2e}, 半径r={radius:.3f}AU, 速度v={velocity:.2f}km/s, 质量动量比M/(r*v)={mass_momentum_ratio:.4e}, 角速度阈值5w={angular_velocity_threshold:.4f}, 角动量失衡量={angular_momentum_imbalance:.4e}, 比角动量亏缺={specific_angular_momentum_deficit:.4f}, 角动量异常指数={angular_momentum_anomaly_index:.1f}%"

        if x * y > z / (m + 0.01) + w * 100:
            type_code = 'A4'
            radius_velocity_product = x * y
            mass_angular_eccentricity_term = z / (m + 0.01) + w * 100
            analysis_detail = f"半径速度积与质量比分析: 半径速度积={radius_velocity_product:.3f}, 质量角速度离心率项={mass_angular_eccentricity_term:.3f}, 积超载度={min((radius_velocity_product - mass_angular_eccentricity_term) / mass_angular_eccentricity_term * 20, 95) if mass_angular_eccentricity_term > 0 else 0:.1f}%"

        if z ** 0.5 < m * 5 + x / 10 + y / 10:
            type_code = 'A5'
            mass_root = z ** 0.5
            angular_radius_velocity_sum = m * 5 + x / 10 + y / 10
            analysis_detail = f"质量与角速度开方比较分析: 质量开方={mass_root:.4f}, 角速度半径速度和={angular_radius_velocity_sum:.4f}, 开方缺口度={min((angular_radius_velocity_sum - mass_root) / mass_root * 24, 95) if mass_root > 0 else 0:.1f}%"

        if x * z > y * m * 10 + w * 500:
            type_code = 'A6'
            radius_mass_product = x * z
            velocity_angular_eccentricity = y * m * 10 + w * 500
            analysis_detail = f"半径质量积与速度比分析: 半径质量积={radius_mass_product:.3f}, 速度角速度离心率={velocity_angular_eccentricity:.3f}, 积超载度={min((radius_mass_product - velocity_angular_eccentricity) / velocity_angular_eccentricity * 19, 95) if velocity_angular_eccentricity > 0 else 0:.1f}%"

        if x / (y + 0.1) + z / (w + 0.01) > m * 10 + 5:
            type_code = 'A7'
            reciprocal_orbital_sum = x / (y + 0.1) + z / (w + 0.01)
            angular_threshold = m * 10 + 5
            analysis_detail = f"多变量倒数和分析: 倒数轨道和={reciprocal_orbital_sum:.4f}, 角速度阈值={angular_threshold:.3f}, 倒数和异常度={min((reciprocal_orbital_sum - angular_threshold) / angular_threshold * 22, 95):.1f}%"

        position_velocity_mass_result = comm.recv(source=17, tag=100, status=status)
        orbital_shape_result = comm.recv(source=18, tag=200, status=status)
        gravitational_angular_result = comm.recv(source=19, tag=300, status=status)

        analysis_results = [
            f"宏观轨道稳定性 (r,v,M,e,w): {type_code} -> {CELESTIAL_MECHANICS_TYPE_DEF.get(type_code, '未知')} | {analysis_detail}",
            f"位置速度质量 (r,v,M): {position_velocity_mass_result['code']} -> {CELESTIAL_MECHANICS_TYPE_DEF.get(position_velocity_mass_result['code'], '未知')} | {position_velocity_mass_result['detail']}",
            f"轨道形态 (v,M,e): {orbital_shape_result['code']} -> {CELESTIAL_MECHANICS_TYPE_DEF.get(orbital_shape_result['code'], '未知')} | {orbital_shape_result['detail']}",
            f"引力势能与角动量 (M,e,w): {gravitational_angular_result['code']} -> {CELESTIAL_MECHANICS_TYPE_DEF.get(gravitational_angular_result['code'], '未知')} | {gravitational_angular_result['detail']}"
        ]

        print("=" * 75)
        print("  天体运动模拟系统 (进程 16-19)  ")
        print("=" * 75)
        print()
        print("--- 实时天体系统参数 ---")
        print(f"轨道半径 r (X): {x:.3f} AU")
        print(f"轨道速度 v (Y): {y:.2f} km/s")
        print(f"质量 M (Z): {z:.2e} M_sun")
        print(f"离心率 e (W): {w:.4f}")
        print(f"角速度 w (M): {m:.4f} rad/day")
        print()
        print("--- 天体系统综合分析报告 ---")
        for i, result in enumerate(analysis_results, 1):
            print(f"{i}. {result}")
        print()
        print("=" * 75)
        print(f"程序5 (Ranks 16-19) 分析完成")
        print("=" * 75)
        print("\n")

    elif rank == 17:
        x = comm.recv(source=16, tag=1, status=status)
        y = comm.recv(source=16, tag=2, status=status)
        z = comm.recv(source=16, tag=3, status=status)

        type_code = 'B0'
        analysis_detail = ""

        if y + z / 10 > x * x * 5:
            type_code = 'B1'
            velocity = y
            normalized_mass = z / 10
            velocity_mass_sum = y + z / 10
            radius_squared_scale = x * x * 5
            energy_parameter_excess = velocity_mass_sum - radius_squared_scale
            kinetic_potential_ratio = velocity_mass_sum / radius_squared_scale if radius_squared_scale > 0 else float('inf')
            orbital_energy_anomaly_index = min(kinetic_potential_ratio * 24, 95)
            analysis_detail = f"轨道能量异常分析: 速度v={velocity:.2f}km/s, 归一化质量M/10={normalized_mass:.2e}, 速度质量和={velocity_mass_sum:.2f}, 半径平方尺度5r^2={radius_squared_scale:.3f}, 能量参数超量={energy_parameter_excess:.2f}, 动能势能比={kinetic_potential_ratio:.4f}, 轨道能量异常指数={orbital_energy_anomaly_index:.1f}%"

        if z > x * y and x > 10:
            type_code = 'B2'
            mass = z
            radius = x
            velocity = y
            radius_velocity_product = x * y
            large_mass_excess = mass - radius_velocity_product
            outer_solar_system_criterion = radius
            jovian_planet_parameter = mass / radius_velocity_product if radius_velocity_product > 0 else float('inf')
            outer_system_giant_index = min(jovian_planet_parameter * 18, 95)
            analysis_detail = f"外太阳系大质量天体分析: 质量M={mass:.2e}, 半径r={radius:.3f}AU(外太阳系), 速度v={velocity:.2f}km/s, 半径速度积r*v={radius_velocity_product:.3f}, 大质量超量={large_mass_excess:.2e}, 外系判据r={outer_solar_system_criterion:.3f}AU, 类木行星参数={jovian_planet_parameter:.4f}, 外系巨行星指数={outer_system_giant_index:.1f}%"

        if x > y / (z + 0.01) + 10:
            type_code = 'B3'
            radius = x
            velocity = y
            mass = z
            velocity_mass_ratio = y / (z + 0.01)
            slow_orbit_threshold = velocity_mass_ratio + 10
            large_orbit_excess = radius - slow_orbit_threshold
            slow_motion_parameter = radius / slow_orbit_threshold if slow_orbit_threshold > 0 else float('inf')
            distant_slow_orbit_index = min(slow_motion_parameter * 21, 95)
            analysis_detail = f"大轨道慢速模式分析: 半径r={radius:.3f}AU, 速度v={velocity:.2f}km/s, 质量M={mass:.2e}, 速度质量比v/M={velocity_mass_ratio:.4f}, 慢速轨道阈值={slow_orbit_threshold:.3f}, 大轨道超量={large_orbit_excess:.3f}, 慢速运动参数={slow_motion_parameter:.4f}, 远距慢速轨道指数={distant_slow_orbit_index:.1f}%"

        if y ** 2 > x * z + 100:
            type_code = 'B4'
            velocity_squared = y ** 2
            radius_mass_product = x * z + 100
            analysis_detail = f"速度平方与半径质量积分析: 速度平方={velocity_squared:.3f}, 半径质量积={radius_mass_product:.3f}, 平方超载度={min((velocity_squared - radius_mass_product) / radius_mass_product * 21, 95) if radius_mass_product > 0 else 0:.1f}%"

        if z ** 0.5 + x / 10 < y * 2 + 10:
            type_code = 'B5'
            mass_root_radius = z ** 0.5 + x / 10
            velocity_linear_baseline = y * 2 + 10
            analysis_detail = f"质量开方与半径速度和分析: 质量开方半径={mass_root_radius:.4f}, 速度线性基线={velocity_linear_baseline:.3f}, 组合缺口度={min((velocity_linear_baseline - mass_root_radius) / mass_root_radius * 26, 95) if mass_root_radius > 0 else 0:.1f}%"

        if x * y / (z ** 0.5 + 0.01) > 50:
            type_code = 'B6'
            radius_velocity_mass_ratio = x * y / (z ** 0.5 + 0.01)
            ratio_threshold = 50
            analysis_detail = f"半径速度与质量开方比分析: 半径速度质量比={radius_velocity_mass_ratio:.3f}, 比值阈值={ratio_threshold}, 比值超载度={min((radius_velocity_mass_ratio - ratio_threshold) / ratio_threshold * 18, 95):.1f}%"

        if x ** 0.5 + y ** 0.6 > z ** 0.3 + 15:
            type_code = 'B7'
            fractional_power_orbital_sum = x ** 0.5 + y ** 0.6
            mass_power_baseline = z ** 0.3 + 15
            analysis_detail = f"半径速度分数幂和分析: 分数幂轨道和={fractional_power_orbital_sum:.3f}, 质量幂基线={mass_power_baseline:.3f}, 分数幂超载度={min((fractional_power_orbital_sum - mass_power_baseline) / mass_power_baseline * 23, 95) if mass_power_baseline > 0 else 0:.1f}%"

        result = {'code': type_code, 'detail': analysis_detail}
        comm.send(result, dest=16, tag=100)

    elif rank == 18:
        y = comm.recv(source=16, tag=1, status=status)
        z = comm.recv(source=16, tag=2, status=status)
        w = comm.recv(source=16, tag=3, status=status)

        type_code = 'C0'
        analysis_detail = ""

        if w * 100 < z / y:
            type_code = 'C1'
            eccentricity = w
            eccentricity_scaled = w * 100
            mass = z
            velocity = y
            mass_velocity_ratio = z / y if y > 0 else float('inf')
            circular_orbit_criterion = mass_velocity_ratio - eccentricity_scaled
            circularity_parameter = mass_velocity_ratio / eccentricity_scaled if eccentricity_scaled > 0 else float('inf')
            near_circular_orbit_index = min(circularity_parameter / 10, 95)
            analysis_detail = f"近圆轨道特征分析: 离心率e={eccentricity:.4f}, 放大离心率100e={eccentricity_scaled:.2f}, 质量M={mass:.2e}, 速度v={velocity:.2f}km/s, 质量速度比M/v={mass_velocity_ratio:.4e}, 圆轨道判据={circular_orbit_criterion:.4e}, 圆度参数={circularity_parameter:.4f}, 近圆轨道指数={near_circular_orbit_index:.1f}%"

        if w > 0.5 and y < z / 20:
            type_code = 'C2'
            eccentricity = w
            velocity = y
            mass = z
            high_eccentricity_threshold = 0.5
            mass_velocity_threshold = z / 20
            elliptical_excess = eccentricity - high_eccentricity_threshold
            slow_motion_deficit = mass_velocity_threshold - velocity
            ellipticity_parameter = eccentricity / 0.5
            elliptical_slow_orbit_index = min(ellipticity_parameter * 30, 95)
            analysis_detail = f"椭圆慢速轨道分析: 离心率e={eccentricity:.4f}(高椭圆), 速度v={velocity:.2f}km/s, 质量M={mass:.2e}, 高离心率阈值={high_eccentricity_threshold}, 质量速度阈值M/20={mass_velocity_threshold:.4f}, 椭圆度超量={elliptical_excess:.4f}, 慢速亏缺={slow_motion_deficit:.2f}, 椭圆度参数={ellipticity_parameter:.4f}, 椭圆慢速轨道指数={elliptical_slow_orbit_index:.1f}%"

        if y > z * 20 and y - z > w * 50:
            type_code = 'C3'
            velocity = y
            mass = z
            eccentricity = w
            high_velocity_threshold = z * 20
            velocity_excess = velocity - high_velocity_threshold
            velocity_mass_difference = y - z
            eccentricity_scaled_threshold = w * 50
            difference_excess = velocity_mass_difference - eccentricity_scaled_threshold
            cometary_parameter = velocity / (mass * 20) if mass > 0 else float('inf')
            cometary_orbit_index = min(cometary_parameter * 15, 95)
            analysis_detail = f"彗星型轨道分析: 速度v={velocity:.2f}km/s(高速), 质量M={mass:.2e}(小质量), 离心率e={eccentricity:.4f}, 高速阈值20M={high_velocity_threshold:.4f}, 速度超量={velocity_excess:.2f}, 速度质量差v-M={velocity_mass_difference:.2f}, 离心率尺度50e={eccentricity_scaled_threshold:.2f}, 差值超量={difference_excess:.2f}, 彗星参数={cometary_parameter:.4f}, 彗星型轨道指数={cometary_orbit_index:.1f}%"

        if (y * z) ** 0.5 < w * 500 + 10:
            type_code = 'C4'
            velocity_mass_geometric = (y * z) ** 0.5
            eccentricity_baseline = w * 500 + 10
            analysis_detail = f"速度质量几何平均分析: 速度质量几何平均={velocity_mass_geometric:.3f}, 离心率基线={eccentricity_baseline:.3f}, 几何平均不足度={min((eccentricity_baseline - velocity_mass_geometric) / velocity_mass_geometric * 25, 95) if velocity_mass_geometric > 0 else 0:.1f}%"

        if y ** 2 + z * w > 1000:
            type_code = 'C5'
            velocity_mass_aggregate = y ** 2 + z * w
            aggregate_threshold = 1000
            analysis_detail = f"速度平方加质量离心率积分析: 速度质量聚合={velocity_mass_aggregate:.3f}, 聚合阈值={aggregate_threshold}, 聚合超载度={min((velocity_mass_aggregate - aggregate_threshold) / aggregate_threshold * 20, 95):.1f}%"

        if ((y - z) ** 2) ** 0.5 + w * 10 > 15:
            type_code = 'C6'
            velocity_mass_diff_magnitude = ((y - z) ** 2) ** 0.5 + w * 10
            diff_threshold = 15
            analysis_detail = f"速度质量差平方开方分析: 速度质量差量级={velocity_mass_diff_magnitude:.3f}, 差值阈值={diff_threshold}, 差值异常度={min((velocity_mass_diff_magnitude - diff_threshold) / diff_threshold * 23, 95):.1f}%"

        result = {'code': type_code, 'detail': analysis_detail}
        comm.send(result, dest=16, tag=200)

    elif rank == 19:
        z = comm.recv(source=16, tag=1, status=status)
        w = comm.recv(source=16, tag=2, status=status)
        m = comm.recv(source=16, tag=3, status=status)

        type_code = 'D0'
        analysis_detail = ""

        if z > m * w * 100:
            type_code = 'D1'
            mass = z
            angular_velocity = m
            eccentricity = w
            angular_eccentricity_product = m * w * 100
            mass_dominance_excess = mass - angular_eccentricity_product
            gravitational_dominance_ratio = mass / angular_eccentricity_product if angular_eccentricity_product > 0 else float('inf')
            massive_body_dominance_index = min(gravitational_dominance_ratio * 23, 95)
            analysis_detail = f"大质量主导系统分析: 质量M={mass:.2e}, 角速度w={angular_velocity:.4f}rad/day, 离心率e={eccentricity:.4f}, 角速度离心率积100w*e={angular_eccentricity_product:.4f}, 质量主导超量={mass_dominance_excess:.2e}, 引力主导比={gravitational_dominance_ratio:.4f}, 大质量天体主导指数={massive_body_dominance_index:.1f}%"

        if m + w > z * 0.01:
            type_code = 'D2'
            angular_velocity = m
            eccentricity = w
            mass = z
            orbital_parameter_sum = m + w
            mass_scaled = z * 0.01
            parameter_dominance_excess = orbital_parameter_sum - mass_scaled
            orbital_configuration_ratio = orbital_parameter_sum / mass_scaled if mass_scaled > 0 else float('inf')
            orbital_parameter_dominance_index = min(orbital_configuration_ratio * 20, 95)
            analysis_detail = f"轨道参数和主导分析: 角速度w={angular_velocity:.4f}rad/day, 离心率e={eccentricity:.4f}, 质量M={mass:.2e}, 轨道参数和w+e={orbital_parameter_sum:.4f}, 质量尺度0.01M={mass_scaled:.2e}, 参数主导超量={parameter_dominance_excess:.4f}, 轨道配置比={orbital_configuration_ratio:.4f}, 轨道参数主导指数={orbital_parameter_dominance_index:.1f}%"

        if w < m / z and m > 1:
            type_code = 'D3'
            eccentricity = w
            angular_velocity = m
            mass = z
            angular_mass_ratio = m / z if z > 0 else float('inf')
            low_eccentricity_criterion = angular_mass_ratio
            circularity_deficit = low_eccentricity_criterion - eccentricity
            fast_rotation_threshold = 1
            rotation_excess = angular_velocity - fast_rotation_threshold
            co_orbital_parameter = angular_velocity / (eccentricity + 0.001) if eccentricity > 0 else float('inf')
            fast_circular_co_orbital_index = min(co_orbital_parameter / 100, 95)
            analysis_detail = f"快速圆轨道共轨态分析: 离心率e={eccentricity:.4f}(低), 角速度w={angular_velocity:.4f}rad/day(高), 质量M={mass:.2e}, 角速度质量比w/M={angular_mass_ratio:.4f}, 低离心率判据={low_eccentricity_criterion:.4f}, 圆度亏缺={circularity_deficit:.4f}, 快速旋转阈值={fast_rotation_threshold}, 转速超量={rotation_excess:.4f}, 共轨参数={co_orbital_parameter:.2f}, 快速圆轨道共轨指数={fast_circular_co_orbital_index:.1f}%"

        if z * w / (m + 0.01) > 50:
            type_code = 'D4'
            mass_eccentricity_angular_ratio = z * w / (m + 0.01)
            ratio_threshold = 50
            analysis_detail = f"质量离心率积与角速度比分析: 质量离心率角速度比={mass_eccentricity_angular_ratio:.3f}, 比值阈值={ratio_threshold}, 比值超载度={min((mass_eccentricity_angular_ratio - ratio_threshold) / ratio_threshold * 22, 95):.1f}%"

        if m ** 0.5 < z ** 0.3 + w * 5 + 2:
            type_code = 'D5'
            angular_root = m ** 0.5
            mass_eccentricity_sum = z ** 0.3 + w * 5 + 2
            analysis_detail = f"角速度开方与质量离心率和分析: 角速度开方={angular_root:.3f}, 质量离心率和={mass_eccentricity_sum:.3f}, 角速度不足度={min((mass_eccentricity_sum - angular_root) / angular_root * 28, 95) if angular_root > 0 else 0:.1f}%"

        if w ** 0.6 * m ** 0.5 > z ** 0.2 + 5:
            type_code = 'D6'
            eccentricity_angular_power = w ** 0.6 * m ** 0.5
            mass_power_baseline = z ** 0.2 + 5
            analysis_detail = f"离心率角速度分数幂积分析: 离心率角速度幂积={eccentricity_angular_power:.3f}, 质量幂基线={mass_power_baseline:.3f}, 幂积超载度={min((eccentricity_angular_power - mass_power_baseline) / mass_power_baseline * 19, 95) if mass_power_baseline > 0 else 0:.1f}%"

        result = {'code': type_code, 'detail': analysis_detail}
        comm.send(result, dest=16, tag=300)

    elif rank == 20:
        x = random.uniform(0.0, 1000.0)  # 应力 σ (MPa)
        y = random.uniform(0.0, 0.5)  # 应变 ε
        z = random.uniform(1.0, 500.0)  # 弹性模量 E (GPa)
        w = random.uniform(0.1, 0.5)  # 泊松比 ν
        m = random.uniform(0.0, 500.0)  # 剪切应力 τ (MPa)

        comm.send(x, dest=21, tag=1); comm.send(y, dest=21, tag=2); comm.send(z, dest=21, tag=3)
        comm.send(y, dest=22, tag=1); comm.send(z, dest=22, tag=2); comm.send(w, dest=22, tag=3)
        comm.send(z, dest=23, tag=1); comm.send(w, dest=23, tag=2); comm.send(m, dest=23, tag=3)

        type_code = 'A0'
        analysis_detail = ""

        if x > z * y + 100:
            type_code = 'A1'
            stress = x
            elastic_modulus = z
            strain = y
            hooke_prediction = z * y
            deviation_threshold = 100
            theoretical_stress = hooke_prediction + deviation_threshold
            stress_excess = stress - theoretical_stress
            nonlinearity_factor = stress / theoretical_stress if theoretical_stress > 0 else float('inf')
            plastic_deformation_index = min((nonlinearity_factor - 1) * 100, 95)
            analysis_detail = f"胡克定律偏离分析: 应力σ={stress:.2f}MPa, 弹性模量E={elastic_modulus:.2f}GPa, 应变ε={strain:.6f}, 胡克预测E*ε={hooke_prediction:.2f}MPa, 偏离阈值={deviation_threshold}MPa, 理论应力={theoretical_stress:.2f}MPa, 应力超量={stress_excess:.2f}MPa, 非线性因子={nonlinearity_factor:.4f}, 塑性变形指数={plastic_deformation_index:.1f}%"

        if m / (x + 0.1) > 0.8 or w > 0.45:
            type_code = 'A2'
            shear_stress = m
            normal_stress = x
            poisson_ratio = w
            shear_stress_ratio = m / (x + 0.1)
            shear_dominance_threshold = 0.8
            incompressibility_threshold = 0.45
            material_type = ""
            if shear_stress_ratio > 0.8:
                material_type = "剪切主导模式"
                shear_stress_index = min((shear_stress_ratio / shear_dominance_threshold) * 50, 95)
            else:
                material_type = "不可压缩材料"
                shear_stress_index = min((poisson_ratio / incompressibility_threshold) * 50, 95)
            analysis_detail = f"剪切主导或不可压缩材料分析: 剪切应力τ={shear_stress:.2f}MPa, 正应力σ={normal_stress:.2f}MPa, 泊松比ν={poisson_ratio:.4f}, 剪应力比τ/σ={shear_stress_ratio:.4f}, 剪切阈值={shear_dominance_threshold}, 不可压缩阈值={incompressibility_threshold}, 材料类型={material_type}, 特征指数={shear_stress_index:.1f}%"

        if x + m > y * z * 2:
            type_code = 'A3'
            normal_stress = x
            shear_stress = m
            total_stress = x + m
            strain = y
            elastic_modulus = z
            strain_capacity_doubled = y * z * 2
            total_stress_excess = total_stress - strain_capacity_doubled
            stress_state_ratio = total_stress / strain_capacity_doubled if strain_capacity_doubled > 0 else float('inf')
            combined_stress_anomaly = min((stress_state_ratio - 1) * 80, 95)
            analysis_detail = f"总应力状态异常分析: 正应力σ={normal_stress:.2f}MPa, 剪切应力τ={shear_stress:.2f}MPa, 总应力σ+τ={total_stress:.2f}MPa, 应变ε={strain:.6f}, 弹性模量E={elastic_modulus:.2f}GPa, 应变能力双倍2ε*E={strain_capacity_doubled:.2f}MPa, 总应力超量={total_stress_excess:.2f}MPa, 应力状态比={stress_state_ratio:.4f}, 组合应力异常度={combined_stress_anomaly:.1f}%"

        if x * y > z / 10 + m:
            type_code = 'A4'
            stress_strain_product = x * y
            modulus_shear_term = z / 10 + m
            analysis_detail = f"应力应变积与模量比分析: 应力应变积={stress_strain_product:.3f}, 模量剪切项={modulus_shear_term:.3f}, 积超载度={min((stress_strain_product - modulus_shear_term) / modulus_shear_term * 20, 95) if modulus_shear_term > 0 else 0:.1f}%"

        if z ** 0.5 < w * 50 + x / 100 + y * 100:
            type_code = 'A5'
            modulus_root = z ** 0.5
            poisson_stress_strain_sum = w * 50 + x / 100 + y * 100
            analysis_detail = f"模量开方与泊松比关系分析: 模量开方={modulus_root:.3f}, 泊松应力应变和={poisson_stress_strain_sum:.3f}, 开方缺口度={min((poisson_stress_strain_sum - modulus_root) / modulus_root * 24, 95) if modulus_root > 0 else 0:.1f}%"

        if x * z > y * 10000 + m * 100:
            type_code = 'A6'
            stress_modulus_product = x * z
            strain_shear_term = y * 10000 + m * 100
            analysis_detail = f"应力模量积与剪切比分析: 应力模量积={stress_modulus_product:.3f}, 应变剪切项={strain_shear_term:.3f}, 积超载度={min((stress_modulus_product - strain_shear_term) / strain_shear_term * 19, 95) if strain_shear_term > 0 else 0:.1f}%"

        if x / (y + 0.001) + z / (w + 0.1) > m * 5 + 500:
            type_code = 'A7'
            reciprocal_stress_sum = x / (y + 0.001) + z / (w + 0.1)
            shear_threshold = m * 5 + 500
            analysis_detail = f"多变量倒数和分析: 倒数应力和={reciprocal_stress_sum:.3f}, 剪切阈值={shear_threshold:.3f}, 倒数和异常度={min((reciprocal_stress_sum - shear_threshold) / shear_threshold * 22, 95):.1f}%"

        stress_strain_modulus_result = comm.recv(source=21, tag=100, status=status)
        material_parameters_result = comm.recv(source=22, tag=200, status=status)
        failure_criterion_result = comm.recv(source=23, tag=300, status=status)

        analysis_results = [
            f"宏观力学响应 (σ,ε,E,ν,τ): {type_code} -> {MATERIAL_STRESS_TYPE_DEF.get(type_code, '未知')} | {analysis_detail}",
            f"应力应变模量 (σ,ε,E): {stress_strain_modulus_result['code']} -> {MATERIAL_STRESS_TYPE_DEF.get(stress_strain_modulus_result['code'], '未知')} | {stress_strain_modulus_result['detail']}",
            f"材料性能参数 (ε,E,ν): {material_parameters_result['code']} -> {MATERIAL_STRESS_TYPE_DEF.get(material_parameters_result['code'], '未知')} | {material_parameters_result['detail']}",
            f"破坏准则 (E,ν,τ): {failure_criterion_result['code']} -> {MATERIAL_STRESS_TYPE_DEF.get(failure_criterion_result['code'], '未知')} | {failure_criterion_result['detail']}"
        ]

        print("=" * 75)
        print("  材料应力分析系统 (进程 20-23)  ")
        print("=" * 75)
        print()
        print("--- 实时材料应力参数 ---")
        print(f"应力 σ (X): {x:.2f} MPa")
        print(f"应变 ε (Y): {y:.6f}")
        print(f"弹性模量 E (Z): {z:.2f} GPa")
        print(f"泊松比 ν (W): {w:.4f}")
        print(f"剪切应力 τ (M): {m:.2f} MPa")
        print()
        print("--- 材料应力综合分析报告 ---")
        for i, result in enumerate(analysis_results, 1):
            print(f"{i}. {result}")
        print()
        print("=" * 75)
        print(f"程序6 (Ranks 20-23) 分析完成")
        print("=" * 75)
        print("\n")

    elif rank == 21:
        x = comm.recv(source=20, tag=1, status=status)
        y = comm.recv(source=20, tag=2, status=status)
        z = comm.recv(source=20, tag=3, status=status)

        type_code = 'B0'
        analysis_detail = ""

        if y * 1000 > x and y < 0.005:
            type_code = 'B1'
            strain = y
            strain_scaled = y * 1000
            stress = x
            small_strain_threshold = 0.005
            elastic_sensitivity = strain_scaled / stress if stress > 0 else float('inf')
            high_sensitivity_parameter = strain_scaled - stress
            elastic_precision_index = min(elastic_sensitivity * 10, 95)
            analysis_detail = f"弹性变形高灵敏度分析: 应变ε={strain:.6f}, 应变放大1000ε={strain_scaled:.3f}, 应力σ={stress:.2f}MPa, 小应变阈值={small_strain_threshold}, 弹性灵敏度1000ε/σ={elastic_sensitivity:.6f}, 高灵敏参数={high_sensitivity_parameter:.3f}, 弹性精度指数={elastic_precision_index:.1f}%"

        if z > (x + y * 100) * 2:
            type_code = 'B2'
            elastic_modulus = z
            stress = x
            strain = y
            strain_scaled = y * 100
            stress_strain_sum = x + y * 100
            rigidity_threshold = stress_strain_sum * 2
            modulus_excess = elastic_modulus - rigidity_threshold
            rigidity_factor = elastic_modulus / rigidity_threshold if rigidity_threshold > 0 else float('inf')
            stiff_material_index = min((rigidity_factor - 1) * 50, 95)
            analysis_detail = f"刚性材料特征分析: 弹性模量E={elastic_modulus:.2f}GPa, 应力σ={stress:.2f}MPa, 应变ε={strain:.6f}, 应变放大100ε={strain_scaled:.4f}, 应力应变和σ+100ε={stress_strain_sum:.2f}, 刚性阈值2(σ+100ε)={rigidity_threshold:.2f}, 模量超量={modulus_excess:.2f}GPa, 刚性因子={rigidity_factor:.4f}, 刚性材料指数={stiff_material_index:.1f}%"

        if x / (z * y + 0.0001) > 500:
            type_code = 'B3'
            stress = x
            elastic_modulus = z
            strain = y
            hooke_denominator = z * y + 0.0001
            constitutive_ratio = x / hooke_denominator
            severe_deviation_threshold = 500
            deviation_excess = constitutive_ratio - severe_deviation_threshold
            nonlinear_behavior_factor = constitutive_ratio / severe_deviation_threshold
            constitutive_deviation_index = min((nonlinear_behavior_factor - 1) * 30, 95)
            analysis_detail = f"本构关系严重偏离分析: 应力σ={stress:.2f}MPa, 弹性模量E={elastic_modulus:.2f}GPa, 应变ε={strain:.6f}, 胡克分母E*ε={hooke_denominator:.6f}, 本构比σ/(E*ε)={constitutive_ratio:.2f}, 严重偏离阈值={severe_deviation_threshold}, 偏离超量={deviation_excess:.2f}, 非线性行为因子={nonlinear_behavior_factor:.4f}, 本构偏离指数={constitutive_deviation_index:.1f}%"

        if x ** 2 > y * z * 1000 + 10000:
            type_code = 'B4'
            stress_squared = x ** 2
            strain_modulus_product = y * z * 1000 + 10000
            analysis_detail = f"应力平方与应变模量积分析: 应力平方={stress_squared:.3f}, 应变模量积={strain_modulus_product:.3f}, 平方超载度={min((stress_squared - strain_modulus_product) / strain_modulus_product * 21, 95) if strain_modulus_product > 0 else 0:.1f}%"

        if z ** 0.5 + x / 100 < y * 200 + 20:
            type_code = 'B5'
            modulus_root_stress = z ** 0.5 + x / 100
            strain_linear_baseline = y * 200 + 20
            analysis_detail = f"模量开方与应力应变和分析: 模量开方应力={modulus_root_stress:.3f}, 应变线性基线={strain_linear_baseline:.3f}, 组合缺口度={min((strain_linear_baseline - modulus_root_stress) / modulus_root_stress * 26, 95) if modulus_root_stress > 0 else 0:.1f}%"

        if x * y / (z ** 0.5 + 0.1) > 100:
            type_code = 'B6'
            stress_strain_modulus_ratio = x * y / (z ** 0.5 + 0.1)
            ratio_threshold = 100
            analysis_detail = f"应力应变与模量开方比分析: 应力应变模量比={stress_strain_modulus_ratio:.3f}, 比值阈值={ratio_threshold}, 比值超载度={min((stress_strain_modulus_ratio - ratio_threshold) / ratio_threshold * 18, 95):.1f}%"

        if x ** 0.5 + y ** 0.6 * 100 > z ** 0.4 + 50:
            type_code = 'B7'
            fractional_power_stress_sum = x ** 0.5 + y ** 0.6 * 100
            modulus_power_baseline = z ** 0.4 + 50
            analysis_detail = f"应力应变分数幂和分析: 分数幂应力和={fractional_power_stress_sum:.3f}, 模量幂基线={modulus_power_baseline:.3f}, 分数幂超载度={min((fractional_power_stress_sum - modulus_power_baseline) / modulus_power_baseline * 23, 95) if modulus_power_baseline > 0 else 0:.1f}%"

        result = {'code': type_code, 'detail': analysis_detail}
        comm.send(result, dest=20, tag=100)

    elif rank == 22:
        y = comm.recv(source=20, tag=1, status=status)
        z = comm.recv(source=20, tag=2, status=status)
        w = comm.recv(source=20, tag=3, status=status)

        type_code = 'C0'
        analysis_detail = ""

        if z > y * 2000 + w * 100:
            type_code = 'C1'
            elastic_modulus = z
            strain = y
            poisson_ratio = w
            strain_contribution = y * 2000
            poisson_contribution = w * 100
            combined_threshold = strain_contribution + poisson_contribution
            modulus_dominance = elastic_modulus - combined_threshold
            high_modulus_ratio = elastic_modulus / combined_threshold if combined_threshold > 0 else float('inf')
            high_stiffness_material_index = min((high_modulus_ratio - 1) * 40, 95)
            analysis_detail = f"高模量材料分析: 弹性模量E={elastic_modulus:.2f}GPa, 应变ε={strain:.6f}, 泊松比ν={poisson_ratio:.4f}, 应变贡献2000ε={strain_contribution:.3f}, 泊松贡献100ν={poisson_contribution:.2f}, 组合阈值={combined_threshold:.2f}, 模量主导度={modulus_dominance:.2f}GPa, 高模量比={high_modulus_ratio:.4f}, 高刚度材料指数={high_stiffness_material_index:.1f}%"

        if z / (w * 10) > y * 200 + 50:
            type_code = 'C2'
            elastic_modulus = z
            poisson_ratio = w
            strain = y
            normalized_stiffness = z / (w * 10) if w > 0 else float('inf')
            strain_scaled_threshold = y * 200 + 50
            stiffness_excess = normalized_stiffness - strain_scaled_threshold
            over_stiff_ratio = normalized_stiffness / strain_scaled_threshold if strain_scaled_threshold > 0 else float('inf')
            ceramic_brittleness_index = min((over_stiff_ratio - 1) * 30, 95)
            analysis_detail = f"过刚性材料判据分析: 弹性模量E={elastic_modulus:.2f}GPa, 泊松比ν={poisson_ratio:.4f}, 应变ε={strain:.6f}, 归一化刚度E/(10ν)={normalized_stiffness:.2f}, 应变放大阈值200ε+50={strain_scaled_threshold:.2f}, 刚度超量={stiffness_excess:.2f}, 过刚比={over_stiff_ratio:.4f}, 陶瓷脆性指数={ceramic_brittleness_index:.1f}%"

        if y * z < w * 200:
            type_code = 'C3'
            strain = y
            elastic_modulus = z
            poisson_ratio = w
            strain_modulus_product = y * z
            poisson_scaled_threshold = w * 200
            stiffness_deficit = poisson_scaled_threshold - strain_modulus_product
            compliance_ratio = poisson_scaled_threshold / strain_modulus_product if strain_modulus_product > 0 else float('inf')
            compliant_material_index = min((compliance_ratio - 1) * 35, 95)
            analysis_detail = f"低刚度高泊松比材料分析: 应变ε={strain:.6f}, 弹性模量E={elastic_modulus:.2f}GPa, 泊松比ν={poisson_ratio:.4f}, 应变模量积ε*E={strain_modulus_product:.4f}, 泊松比标度200ν={poisson_scaled_threshold:.2f}, 刚度亏缺={stiffness_deficit:.4f}, 柔顺比={compliance_ratio:.4f}, 柔性材料指数={compliant_material_index:.1f}%"

        if (y * z) ** 0.5 < w * 100 + 5:
            type_code = 'C4'
            strain_modulus_geometric = (y * z) ** 0.5
            poisson_baseline = w * 100 + 5
            analysis_detail = f"应变模量几何平均分析: 应变模量几何平均={strain_modulus_geometric:.3f}, 泊松比基线={poisson_baseline:.3f}, 几何平均不足度={min((poisson_baseline - strain_modulus_geometric) / strain_modulus_geometric * 25, 95) if strain_modulus_geometric > 0 else 0:.1f}%"

        if y ** 2 * 10000 + z * w > 500:
            type_code = 'C5'
            strain_modulus_aggregate = y ** 2 * 10000 + z * w
            aggregate_threshold = 500
            analysis_detail = f"应变平方加模量泊松比积分析: 应变模量聚合={strain_modulus_aggregate:.3f}, 聚合阈值={aggregate_threshold}, 聚合超载度={min((strain_modulus_aggregate - aggregate_threshold) / aggregate_threshold * 20, 95):.1f}%"

        if ((y * 100 - z) ** 2) ** 0.5 + w * 10 > 50:
            type_code = 'C6'
            strain_modulus_diff_magnitude = ((y * 100 - z) ** 2) ** 0.5 + w * 10
            diff_threshold = 50
            analysis_detail = f"应变模量差平方开方分析: 应变模量差量级={strain_modulus_diff_magnitude:.3f}, 差值阈值={diff_threshold}, 差值异常度={min((strain_modulus_diff_magnitude - diff_threshold) / diff_threshold * 23, 95):.1f}%"

        if y ** 0.5 * 10 + z ** 0.4 + w ** 0.6 * 10 < 30:
            type_code = 'C7'
            three_variable_material_power_sum = y ** 0.5 * 10 + z ** 0.4 + w ** 0.6 * 10
            power_threshold = 30
            analysis_detail = f"三变量分数幂和分析: 三变量材料幂和={three_variable_material_power_sum:.3f}, 幂和阈值={power_threshold}, 幂和不足度={min((power_threshold - three_variable_material_power_sum) / three_variable_material_power_sum * 27, 95) if three_variable_material_power_sum > 0 else 0:.1f}%"

        result = {'code': type_code, 'detail': analysis_detail}
        comm.send(result, dest=20, tag=200)

    elif rank == 23:
        z = comm.recv(source=20, tag=1, status=status)
        w = comm.recv(source=20, tag=2, status=status)
        m = comm.recv(source=20, tag=3, status=status)

        type_code = 'D0'
        analysis_detail = ""

        if m > z / 50 + w * 200:
            type_code = 'D1'
            shear_stress = m
            elastic_modulus = z
            poisson_ratio = w
            modulus_contribution = z / 50
            poisson_contribution = w * 200
            shear_failure_threshold = modulus_contribution + poisson_contribution
            shear_excess = shear_stress - shear_failure_threshold
            shear_failure_ratio = shear_stress / shear_failure_threshold if shear_failure_threshold > 0 else float('inf')
            shear_failure_risk_index = min((shear_failure_ratio - 1) * 60, 95)
            analysis_detail = f"剪切破坏判据分析: 剪切应力τ={shear_stress:.2f}MPa, 弹性模量E={elastic_modulus:.2f}GPa, 泊松比ν={poisson_ratio:.4f}, 模量贡献E/50={modulus_contribution:.4f}, 泊松贡献200ν={poisson_contribution:.2f}, 剪切破坏阈值={shear_failure_threshold:.2f}MPa, 剪切超量={shear_excess:.2f}MPa, 剪切破坏比={shear_failure_ratio:.4f}, 剪切破坏风险指数={shear_failure_risk_index:.1f}%"

        if z / (w * 2 + 0.1) < m * 5:
            type_code = 'D2'
            elastic_modulus = z
            poisson_ratio = w
            shear_stress = m
            denominator = w * 2 + 0.1
            pseudo_shear_modulus = z / denominator
            shear_stress_quintupled = m * 5
            modulus_deficit = shear_stress_quintupled - pseudo_shear_modulus
            shear_inadequacy_ratio = shear_stress_quintupled / pseudo_shear_modulus if pseudo_shear_modulus > 0 else float('inf')
            shear_modulus_insufficiency_index = min((shear_inadequacy_ratio - 1) * 45, 95)
            analysis_detail = f"剪切模量不足分析: 弹性模量E={elastic_modulus:.2f}GPa, 泊松比ν={poisson_ratio:.4f}, 剪切应力τ={shear_stress:.2f}MPa, 分母2ν+0.1={denominator:.4f}, 伪剪切模量E/(2ν+0.1)={pseudo_shear_modulus:.2f}GPa, 剪切应力五倍5τ={shear_stress_quintupled:.2f}MPa, 模量亏缺={modulus_deficit:.2f}, 剪切不足比={shear_inadequacy_ratio:.4f}, 剪切模量不足指数={shear_modulus_insufficiency_index:.1f}%"

        if m * w > z / 20 or m > 300:
            type_code = 'D3'
            shear_stress = m
            poisson_ratio = w
            elastic_modulus = z
            shear_poisson_product = m * w
            modulus_threshold = z / 20
            high_shear_threshold = 300
            failure_mode = ""
            if m * w > z / 20:
                failure_mode = "剪切泊松耦合破坏"
                failure_index = min((shear_poisson_product / modulus_threshold) * 40, 95)
            else:
                failure_mode = "直接剪切破坏"
                failure_index = min((shear_stress / high_shear_threshold) * 50, 95)
            analysis_detail = f"剪切主导破坏模式分析: 剪切应力τ={shear_stress:.2f}MPa, 泊松比ν={poisson_ratio:.4f}, 弹性模量E={elastic_modulus:.2f}GPa, 剪切泊松积τ*ν={shear_poisson_product:.3f}, 模量阈值E/20={modulus_threshold:.2f}, 高剪切阈值={high_shear_threshold}MPa, 破坏模式={failure_mode}, 破坏指数={failure_index:.1f}%"

        if z * w / (m + 0.1) > 5:
            type_code = 'D4'
            modulus_poisson_shear_ratio = z * w / (m + 0.1)
            ratio_threshold = 5
            analysis_detail = f"模量泊松比积与剪切比分析: 模量泊松剪切比={modulus_poisson_shear_ratio:.3f}, 比值阈值={ratio_threshold}, 比值超载度={min((modulus_poisson_shear_ratio - ratio_threshold) / ratio_threshold * 22, 95):.1f}%"

        if m ** 0.5 < z ** 0.3 + w * 50 + 10:
            type_code = 'D5'
            shear_root = m ** 0.5
            modulus_poisson_sum = z ** 0.3 + w * 50 + 10
            analysis_detail = f"剪切开方与模量泊松比和分析: 剪切开方={shear_root:.3f}, 模量泊松和={modulus_poisson_sum:.3f}, 剪切不足度={min((modulus_poisson_sum - shear_root) / shear_root * 28, 95) if shear_root > 0 else 0:.1f}%"

        if w ** 0.6 * m ** 0.5 > z ** 0.2 + 20:
            type_code = 'D6'
            poisson_shear_power = w ** 0.6 * m ** 0.5
            modulus_power_baseline = z ** 0.2 + 20
            analysis_detail = f"泊松剪切分数幂积分析: 泊松剪切幂积={poisson_shear_power:.3f}, 模量幂基线={modulus_power_baseline:.3f}, 幂积超载度={min((poisson_shear_power - modulus_power_baseline) / modulus_power_baseline * 19, 95) if modulus_power_baseline > 0 else 0:.1f}%"

        result = {'code': type_code, 'detail': analysis_detail}
        comm.send(result, dest=20, tag=300)

if __name__ == "__main__":
    main()