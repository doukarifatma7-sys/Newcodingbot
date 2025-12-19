const searchInput = document.getElementById('searchInput');
const searchBtn = document.getElementById('searchBtn');

searchBtn.addEventListener('click', () => performSearch());
searchInput.addEventListener('keypress', (e) => { if (e.key === 'Enter') performSearch(); });

function performSearch() {
  const query = searchInput.value.trim();
  if (!query) { searchInput.focus(); return; }
  alert(`Recherche effectuée pour: "${query}"`);
  console.log(`Recherche: "${query}"`);
}
