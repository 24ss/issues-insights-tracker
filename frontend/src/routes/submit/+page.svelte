<script lang="ts">
  import { goto } from '$app/navigation';

  let title = '';
  let description = '';
  let severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL' = 'LOW';
  let file: File | null = null;
  let message = '';

  async function handleSubmit() {
    message = '';
    const token = localStorage.getItem('token');
    if (!token) {
      message = 'Please log in first.';
      return;
    }

    const fd = new FormData();
    fd.append('title', title);
    fd.append('description', description);
    fd.append('severity', severity);
    if (file) fd.append('file', file);

    try {
      const res = await fetch('http://localhost:8000/api/issues/', {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}` },
        body: fd
      });
      const data = await res.json();

      if (res.ok) {
        message = 'Issue submitted ✔';
        setTimeout(() => goto('/issues'), 1200);
      } else {
        message = data.detail || 'Submission failed.';
      }
    } catch {
      message = 'Server unreachable.';
    }
  }
</script>

<div class="max-w-2xl mx-auto mt-12 p-6 bg-white rounded shadow">
  <h1 class="text-2xl font-bold mb-4">Submit New Issue</h1>

  {#if message}
    <div class="mb-4 text-sm"
         class:text-red-600={!message.includes('✔')}
         class:text-green-600={message.includes('✔')}>
      {message}
    </div>
  {/if}

  <form on:submit|preventDefault={handleSubmit} class="space-y-4">
    <div>
      <label class="block font-semibold mb-1">Title</label>
      <input type="text" bind:value={title} required class="w-full border rounded px-3 py-2" />
    </div>

    <div>
      <label class="block font-semibold mb-1">Description</label>
      <textarea bind:value={description} rows="4" required class="w-full border rounded px-3 py-2" />
    </div>

    <div>
      <label class="block font-semibold mb-1">Severity</label>
      <select bind:value={severity} class="w-full border rounded px-3 py-2">
        <option value="LOW">LOW</option>
        <option value="MEDIUM">MEDIUM</option>
        <option value="HIGH">HIGH</option>
        <option value="CRITICAL">CRITICAL</option>
      </select>
    </div>

    <div>
      <label class="block font-semibold mb-1">Upload File (optional)</label>
      <input type="file" on:change={(e) => file = e.target.files?.[0] || null} />
    </div>

    <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
      Submit Issue
    </button>
  </form>
</div>
