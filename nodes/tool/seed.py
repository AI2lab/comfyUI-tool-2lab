from ..constants import get_name,get_category

class Seed:
  NAME = get_name('seed')
  CATEGORY = get_category("util")
  RETURN_TYPES = ("INT",)
  RETURN_NAMES = ("SEED",)
  OUTPUT_NODE = True
  FUNCTION = "doWork"

  @classmethod
  def INPUT_TYPES(cls):  # pylint: disable = invalid-name, missing-function-docstring
    return {
      "required": {
        "seed": ("INT", {
          "default": -1,
          "min": -1125899906842624,
          "max": 1125899906842624
        }),
      },
    }

  def main(self, seed=0):
    """Returns the passed seed on execution."""
    return (seed,)