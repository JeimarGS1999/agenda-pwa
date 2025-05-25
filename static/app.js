
document.addEventListener('DOMContentLoaded', () => {
  const dayEl = document.getElementById('day');
  const hourEl = document.getElementById('hour');
  const noteEl = document.getElementById('note');
  const saveBtn = document.getElementById('save');
  const notesList = document.getElementById('notes-list');

  saveBtn.onclick = async () => {
    const day = dayEl.value;
    const hour = hourEl.value;
    const text = noteEl.value;
    if (!hour || !text) return alert("Completa todos los campos");

    await fetch('/api/notes', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ day, hour, text })
    });

    loadNotes();
    noteEl.value = "";
  };

  async function loadNotes() {
    const res = await fetch('/api/notes');
    const data = await res.json();
    notesList.innerHTML = '';
    for (const key in data) {
      const li = document.createElement('li');
      li.textContent = `${key.replace('_', ' ')}: ${data[key]}`;
      notesList.appendChild(li);
    }
  }

  loadNotes();

  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/static/service-worker.js');
  }
});
