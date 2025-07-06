<script lang="ts">
  import { onMount } from 'svelte';

  type Item = { severity: string; count: number };

  let loading = true;
  let error   = '';
  let data: Item[] = [];

  onMount(async () => {
    try {
      const token = localStorage.getItem('token');
      const res = await fetch('http://localhost:8000/api/dashboard/severity-counts', {
        headers: { Authorization: `Bearer ${token}` }
      });

      if (!res.ok) {
        error = 'Failed to load data';
        return;
      }
      data = await res.json();          // [{ severity: 'LOW', count: 2 }, …]
    } catch {
      error = 'Server error';
    } finally {
      loading = false;
    }
  });
</script>

<div class="max-w-3xl mx-auto mt-10 p-4">
  <h1 class="text-2xl font-bold mb-4">Dashboard</h1>

  {#if loading}
    <p class="text-gray-500">Loading…</p>

  {:else if error}
    <p class="text-red-600">{error}</p>

  {:else if data.length === 0}
    <p class="text-gray-500">No open issues found.</p>

  {:else}
    <div class="grid sm:grid-cols-2 md:grid-cols-4 gap-4">
      {#each data as item}
        <div class="bg-white shadow rounded p-4 text-center">
          <p class="text-sm text-gray-600">{item.severity}</p>
          <p class="text-3xl font-bold">{item.count}</p>
        </div>
      {/each}
    </div>
  {/if}
</div>
