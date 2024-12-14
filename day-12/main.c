#include <stdio.h>
#include <glib.h>
#include <stdbool.h>


typedef struct Plot {
  size_t row;
  size_t col;
  bool is_marked;
  int perimeter;
  char region;
} Plot;

typedef struct Garden {
  Plot*** grid;
  GHashTable* regions;
  size_t rows;
  size_t cols;
} Garden;

typedef struct Region {
  char region;
  Plot** plots;
  int area;
  int perimeter;
  int price;
} Region;

bool garden_within_bounds(const Garden garden, const size_t row, const size_t col) {
  return row < garden.rows && col < garden.cols;
}

void garden_free(Garden garden) {
  for (int i = 0; i < garden.rows; i++) {
    for (int j = 0; j < garden.cols; j++) {
      Plot* plot = garden.grid[i][j];
      free(plot);
    }
    free(garden.grid[i]);
  }
  free(garden.grid);

  g_hash_table_destroy(garden.regions);
}

void garden_print(Garden garden, bool compact) {
  printf("%lu x %lu Garden\n", garden.rows, garden.cols);

  printf("Unique regions: ");
  const GList* region = g_hash_table_get_keys(garden.regions);
  while (region != NULL) {
    const char* r = region->data;
    printf(" %c ", *r);
    region = region->next;
  }
  printf("\n");

  for (size_t i = 0; i < garden.rows; i++) {
    for (size_t j = 0; j < garden.cols; j++) {
      Plot* plot = garden.grid[i][j];
      if (compact) {
        printf(" %c ", plot->region);
      } else {
        const char is_marked = plot->is_marked ? 'T' : 'F';
        printf("[%lu x %lu]: <Plot(%c %c %d)>\n", i, j, plot->region, is_marked, plot->perimeter);
      }
    }

    printf("\n");
  }
}

GPtrArray* parse(const char* filename) {
  FILE* fd = fopen(filename, "rt");
  if (fd == NULL) {
    char* errmsg = NULL;
    asprintf(&errmsg, "Unable to open %s", filename);
    perror(errmsg);
  }

  GPtrArray* lines = g_ptr_array_new();
  char buf[256];
  while (fgets(buf, sizeof buf, fd) != NULL) {
    // Get rid of newline character
    buf[strlen(buf) - 1] = '\0';
    g_ptr_array_add(lines, strdup(buf));
  }

  return lines;
}

Garden build_garden(const GPtrArray* lines) {
  const size_t rows = lines->len;
  const size_t cols = strlen(g_ptr_array_index(lines, 0));
  Plot*** grid = calloc(sizeof(Plot**), rows);
  GHashTable* regions = g_hash_table_new(g_str_hash, g_str_equal);

  for (size_t i = 0; i < rows; i++) {
    Plot** plots_row = calloc(sizeof(Plot*), cols);
    const char* line = g_ptr_array_index(lines, i);

    for (size_t j = 0; j < cols; j++) {
      // Put this region in the set
      char* region = NULL;
      asprintf(&region, "%c", line[j]);
      g_hash_table_add(regions, region);

      // Plot plot = {.row=i, .col=j, .is_marked=false, .perimeter=0, .region=line[j]};
      // g_array_append_val(row, plot);
      Plot* plot = calloc(sizeof(Plot), 1);
      plot->row = i;
      plot->col = j;
      plot->is_marked = false;
      plot->perimeter = -1;
      plot->region = line[j];
      plots_row[j] = plot;
    }

    grid[i] = plots_row;
  }

  return (Garden){.grid=grid, .regions=regions, .rows=rows, .cols=cols};
}

GPtrArray* crawl(Garden garden, Plot* start) {
  GPtrArray* region_plots = g_ptr_array_new();
  char region = start->region;

  GQueue* q = g_queue_new();

  g_ptr_array_add(region_plots, start);
  start->is_marked = true;
  g_queue_push_tail(q, start);

  while (!g_queue_is_empty(q)) {
    Plot* plot = g_queue_pop_head(q);

    // Get all unmarked neighboring plots of the same region
    size_t neighbor_rows[] = {plot->row - 1, plot->row, plot->row, plot->row + 1};
    size_t neighbor_cols[] = {plot->col, plot->col - 1, plot->col + 1, plot->col};
    plot->perimeter = 0;
    for (int n = 0; n < 4; n++) {
      size_t row = neighbor_rows[n];
      size_t col = neighbor_cols[n];

      bool is_within_bounds = garden_within_bounds(garden, row, col);

      // Calculate perimeter
      // if the neighbor is out of bounds, it is a perimeter
      // if the neighbor is not of the same region, it is a perimeter
      if (!is_within_bounds || garden.grid[row][col]->region != region)
        plot->perimeter += 1;

      if (
        is_within_bounds &&
        garden.grid[row][col]->region == region &&
        !garden.grid[row][col]->is_marked
      ) {
        Plot* neighbor = garden.grid[row][col];
        g_ptr_array_add(region_plots, neighbor);
        neighbor->is_marked = TRUE;
        g_queue_push_tail(q, neighbor);
      }
    }
  }

  return region_plots;
}

Region build_region(GPtrArray* region_plots, char region) {
  Plot** plots = (Plot**)region_plots->pdata;
  int area = region_plots->len;
  int perimeter = 0;
  for (int k = 0; k < area; k++) {
    Plot* plot = plots[k];
    perimeter += plot->perimeter;
  }
  int price = area * perimeter;
  return (Region){.region=region, .plots=plots, .area=area, .perimeter=perimeter, .price=price};
}

int process(Garden garden, bool print_regions) {
  GArray* regions = g_array_new(FALSE, TRUE, sizeof(Region));

  for (size_t i = 0; i < garden.rows; i++) {
    for (size_t j = 0; j < garden.cols; j++) {
      Plot* start = garden.grid[i][j];

      if (!start->is_marked) {
        // region is an array of Plot pointers
        GPtrArray* region_plots = crawl(garden, start);
        Region region = build_region(region_plots, start->region);
        g_array_append_val(regions, region);
      }
    }
  }

  int total_price = 0;
  for (int k = 0; k < regions->len; k++) {
    Region region = g_array_index(regions, Region, k);
    total_price += region.price;

    if (print_regions) {
      printf("Region: area=%d, perimeter=%d, price=%d\n", region.area, region.perimeter, region.price);
      for (int n = 0; n < region.area; n++) {
        Plot* p = region.plots[n];
        const char is_marked = p->is_marked ? 'T' : 'F';
        printf("[%lu x %lu]: <Plot(%c %c %d)>\n", p->row, p->col, p->region, is_marked, p->perimeter);
      }
      puts("");
    }
  }

  g_array_free(regions, FALSE);
  return total_price;
}

int main(const int argc, char* argv[]) {
  if (argc < 2) {
    puts("Usage: build/day-11 [input file]");
    exit(1);
  }
  const char* filename = argv[1];

  GPtrArray* lines = parse(filename);
  Garden garden = build_garden(lines);
  // garden_print(garden, TRUE);
  // puts("");

  int total_price = process(garden, FALSE);
  printf("Total price: %d\n", total_price);

  g_ptr_array_free(lines, TRUE);
  garden_free(garden);
}
