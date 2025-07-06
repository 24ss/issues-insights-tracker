<script lang="ts">
  import { onMount } from 'svelte';

  let issues: any[] = [];

  // fetch once or after every push event
  async function loadIssues() {
    const token = localStorage.getItem('token');
    const res   = await fetch('http://localhost:8000/api/issues/', {
      headers: { Authorization: `Bearer ${token}` }
    });
    issues = await res.json();
  }

  onMount(() => {
    // initial load
    loadIssues();

    // open Server-Sent Events stream
    const es = new EventSource('http://localhost:8000/api/issues/stream');

    es.onmessage = () => {
      // whenever backend pushes a message, refresh the list
      loadIssues();
    };

    // clean-up when component unmounts
    return () => es.close();
  });

  // color helper
  function statusColor(status: string) {
    const m: Record<string, string> = {
      OPEN: 'bg-red-100 text-red-800',
      TRIAGED: 'bg-yellow-100 text-yellow-800',
      IN_PROGRESS: 'bg-blue-100 text-blue-800',
      DONE: 'bg-green-100 text-green-800'
    };
    return m[status] ?? 'bg-gray-100 text-gray-800';
  }
</script>

<div class="max-w-5xl mx-auto mt-6 space-y-4">
  <h1 class="text-2xl font-bold mb-4">All Issues</h1>

  {#if issues.length === 0}
    <p class="text-gray-500">No issues found.</p>
  {/if}

  {#each issues as issue}
    <div class="bg-white p-4 shadow rounded-lg">
      <div class="flex justify-between items-center">
        <div>
          <h2 class="text-lg font-semibold text-gray-800">{issue.title}</h2>
          <p class="text-sm text-gray-500">Reported by user #{issue.reporter_id}</p>
        </div>
        <span class={`text-xs px-2 py-1 rounded ${statusColor(issue.status)}`}>
          {issue.status}
        </span>
      </div>

      <p class="mt-2 text-sm text-gray-700">{issue.description?.slice(0, 100)}...</p>

      <div class="flex justify-between text-sm mt-3 text-gray-600">
        <span class="font-medium">Severity:</span> {issue.severity}
        {#if issue.attachment}
          <a class="text-blue-600 underline" href={`http://localhost:8000/uploads/${issue.attachment}`} target="_blank">
            View Attachment
          </a>
        {/if}
      </div>
    </div>
  {/each}
</div>
