//
// Created by avilay on 12/11/24.
//
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <glib.h>

typedef struct Pair {
  long first;
  long second;
} Pair;

Pair update(long stone) {
  if (stone == 0)
    return (Pair){.first=1, .second=-1};

  char* string_stone = NULL;
  asprintf(&string_stone, "%ld", stone);
  int len = strlen(string_stone);
  if (len % 2 == 0) {
    int mid = len / 2;

    char string_left[mid] = {};
    for (int i = 0; i < mid; i++) {
      string_left[i] = string_stone[i];
    }
    long left = strtol(string_left, NULL, 10);

    char string_right[len - mid] = {};
    for (int i = 0; i < len - mid; i++) {
      string_right[i] = string_stone[mid + i];
    }
    long right = strtol(string_right, NULL, 10);

    return (Pair){.first=left, .second=right};
  }

  return (Pair){.first=stone*2024, .second=-1};
}

int blink(int n_blinks, long stone) {
  Pair new_stones = update(stone);
  if (n_blinks == 1)
    return new_stones.second == -1 ? 1 : 2;

  int num_stones = blink(n_blinks-1, new_stones.first);
  if (new_stones.second != -1)
    num_stones += blink(n_blinks-1, new_stones.second);

  return num_stones;
}

int blink_2(int n_blinks, long stone) {
  GArray* stones = g_array_new_sized(FALSE, TRUE, sizeof(long), 1);
  g_array_append_val(stones, stone);

  GArray* updated_stones = g_array_new_sized(FALSE, TRUE, sizeof(long), 8);
  for (int i = 0; i < stones->len; i++) {
    stone = g_array_index(stones, long, i);
    Pair new_stones = update(stone);
    g_array_append_val(updated_stones, new_stones.first);
    if (new_stones.second != -1)
      g_array_append_val(updated_stones, new_stones.second);
  }
  g_array_free(stones, TRUE);
  g_array_copy(stones, updated_stones);
  g_array_free(updated_stones, TRUE);
}

int main() {
  // long stones[] = {125, 17};
  long stones[] = {4022724, 951333, 0, 21633, 5857, 97, 702, 6};
  int len = 8;
  int n_blinks = 75;
  int num_stones = 0;
  for (int i = 0; i < len; i++) {
    num_stones += blink_2(n_blinks, stones[i]);
  }
  printf("Number of stones: %d", num_stones);
  return 0;
}
