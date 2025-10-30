# lazor_core/solver.py
"""Stage 4: Solver Algorithm

This module implements the backtracking solver for Lazor puzzles.
It generates all possible placements and tests them using the simulator.
"""
from __future__ import annotations
import copy
from typing import List, Tuple, Optional, Dict
from .board import Board
from .models import BlockType
from .simulator import simulate_board


def get_placeable_positions(board: Board) -> List[Tuple[int, int]]:
    """
    获取所有可放置方块的位置。
    
    参数:
        board: 棋盘对象
    
    返回:
        可放置位置 (r, c) 的列表
    """
    positions = []
    for r in range(board.nrows):
        for c in range(board.ncols):
            if board.is_placeable(r, c):
                positions.append((r, c))
    return positions


def get_blocks_to_place(board: Board) -> List[BlockType]:
    """
    获取需要放置的方块列表。
    
    参数:
        board: 棋盘对象
    
    返回:
        需要放置的方块类型列表（例如: [A, A, C]）
    """
    blocks = []
    for block_type, count in board.free_blocks.items():
        blocks.extend([block_type] * count)
    return blocks


def solve(board: Board) -> Optional[Board]:
    """
    求解 Lazor 谜题。
    
    使用 brute-force 方法生成所有可能的放置组合并测试。
    
    参数:
        board: 初始棋盘对象（包含 free_blocks 信息）
    
    返回:
        如果找到解，返回包含放置方案的 Board 对象；
        如果无解，返回 None
    """
    # 获取所有可放置位置和需要放置的方块
    positions = get_placeable_positions(board)
    blocks_to_place = get_blocks_to_place(board)
    
    # 如果没有方块要放置，检查是否已满足目标
    if not blocks_to_place:
        hit_points = simulate_board(board)
        if board.points.issubset(hit_points):
            return board
        return None
    
    # 导入 itertools 用于生成组合
    from itertools import permutations
    
    # 生成所有可能的放置顺序
    # 注意：这里使用 permutations 会导致重复计算
    # 更高效的方法是使用 combinations（如果方块类型相同）
    
    # 简单优化：使用 combinations 对于相同类型的方块
    from itertools import combinations
    
    num_blocks = len(blocks_to_place)
    num_positions = len(positions)
    
    # 生成选择的位置组合
    for pos_combination in combinations(positions, num_blocks):
        # 对于每个位置组合，生成方块的排列
        for block_permutation in set(permutations(blocks_to_place)):
            # 创建新的棋盘副本
            test_board = copy.deepcopy(board)
            
            # 放置方块
            for i, (r, c) in enumerate(pos_combination):
                test_board.place_block(r, c, block_permutation[i])
            
            # 模拟激光
            hit_points = simulate_board(test_board)
            
            # 检查是否满足所有目标点（使用 issubset）
            if board.points.issubset(hit_points):
                return test_board
    
    return None


def solve_optimized(board: Board, debug=False) -> Optional[Board]:
    """
    优化的求解器（处理相同类型方块的重复问题）。
    
    这个版本对性能进行优化，避免测试等效的配置。
    """
    # 获取所有可放置位置和需要放置的方块
    positions = get_placeable_positions(board)
    blocks_to_place = get_blocks_to_place(board)
    
    if debug:
        print(f"可放置位置: {len(positions)}")
        print(f"需要放置的方块: {blocks_to_place}")
    
    # 如果没有方块要放置，检查是否已满足目标
    if not blocks_to_place:
        hit_points = simulate_board(board)
        if board.points.issubset(hit_points):
            return board
        return None
    
    # 优化：按类型分组方块
    from collections import Counter
    block_counts = Counter(blocks_to_place)
    
    # 生成所有可能的放置
    from itertools import combinations, permutations
    
    num_blocks = len(blocks_to_place)
    num_positions = len(positions)
    
    if debug:
        print(f"方块数量: {num_blocks}, 位置数量: {num_positions}")
    
    # 如果方块数量超出位置数量，无解
    if num_blocks > num_positions:
        return None
    
    # 生成所有位置组合
    combo_count = 0
    perm_count = 0
    
    for pos_combo in combinations(positions, num_blocks):
        combo_count += 1
        # 生成方块排列（注意去重处理相同类型）
        # 使用 set 去重
        processed_permutations = set()
        
        for block_perm in permutations(blocks_to_place):
            if block_perm in processed_permutations:
                continue
            processed_permutations.add(block_perm)
            
            perm_count += 1
            
            # 创建测试棋盘
            test_board = copy.deepcopy(board)
            
            # 放置方块
            try:
                for i, (r, c) in enumerate(pos_combo):
                    test_board.place_block(r, c, block_perm[i])
                
                # 模拟激光
                hit_points = simulate_board(test_board)
                
                # 调试输出
                if debug and perm_count % 100 == 0:
                    print(f"  已测试 {perm_count} 个配置...")
                
                # 检查是否满足所有目标（使用 issubset 而不是相等）
                if board.points.issubset(hit_points):
                    if debug:
                        print(f"✓ 找到解！测试了 {combo_count} 个位置组合，{perm_count} 个方块排列")
                    return test_board
            except ValueError:
                # 放置失败，跳过
                continue
    
    if debug:
        print(f"测试了 {combo_count} 个位置组合，{perm_count} 个方块排列")
    
    return None

