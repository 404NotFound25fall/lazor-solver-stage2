
# lazor_core/__init__.py
from .models import BlockType, Block, Laser, BFFSpec
from .board import Board
from .parser import parse_bff
from .simulator import simulate_board
from .solver import solve, solve_optimized, get_placeable_positions, get_blocks_to_place

__all__ = [
    "BlockType", "Block", "Laser", "BFFSpec", 
    "Board", "parse_bff", 
    "simulate_board", 
    "solve", "solve_optimized",
    "get_placeable_positions", "get_blocks_to_place"
]
