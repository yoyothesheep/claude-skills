#!/usr/bin/env python3
"""Random inspiration draws for concept ideation.

Usage: python3 concept_draws.py [count]   (default 20)

Each draw pairs two random sources from different pools; no source repeats across draws.
Every concept must grow out of one draw.
"""
import secrets
import sys

POOLS = {
    "craft": ["letterpress", "weaving", "ceramics", "bookbinding", "stained glass", "origami",
              "woodblock print", "embroidery", "glassblowing", "marquetry", "basketry", "enamel pins"],
    "place": ["tide pool", "night train", "greenhouse", "laundromat", "observatory", "ski lodge",
              "harbor", "botanical garden", "airport lounge", "bathhouse", "corner bodega", "lighthouse"],
    "era": ["1920s Bauhaus", "1960s space race", "Edo period", "1980s Memphis", "Art Nouveau",
            "1970s public TV", "Victorian almanac", "1990s Tamagotchi", "Mid-century Scandinavia",
            "Y2K chrome", "Soviet modernism", "Ancient Roman mosaic"],
    "material": ["frosted glass", "terrazzo", "cork", "felt", "brushed aluminum", "rice paper",
                 "beeswax", "linen", "copper patina", "acrylic", "slate", "washi tape"],
    "game": ["solitaire", "Tetris", "board-game tokens", "pinball", "crossword", "Animal Crossing",
             "dominoes", "Go stones", "trading cards", "point-and-click adventure", "mahjong", "jigsaw"],
    "profession": ["cartographer", "air-traffic controller", "florist", "librarian", "sommelier",
                   "watchmaker", "beekeeper", "typesetter", "meteorologist", "park ranger",
                   "set designer", "nurse"],
    "nature": ["lichen", "monsoon", "coral", "aurora", "dunes", "fog bank", "tree rings",
               "migrating birds", "tidal flats", "volcanic glass", "moss", "frost ferns"],
    "object": ["train ticket", "seed packet", "tide table", "matchbox", "postage stamp",
               "museum audio guide", "thermostat", "cassette J-card", "luggage tag",
               "recipe card box", "hotel key", "weather vane"],
}


def main():
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    rng = secrets.SystemRandom()
    left = {name: rng.sample(items, len(items)) for name, items in POOLS.items()}
    for i in range(1, count + 1):
        a, b = rng.sample([n for n in left if left[n]], 2)
        print(f"{i}. {left[a].pop()} + {left[b].pop()}")


if __name__ == "__main__":
    main()
