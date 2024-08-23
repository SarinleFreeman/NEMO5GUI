document.addEventListener('DOMContentLoaded', function() {
    // Toggle for optional fields
    const toggleOptionalFields = document.getElementById('toggleOptionalFields');
    const optionalFields = document.getElementById('optionalFields');
    if (toggleOptionalFields && optionalFields) {
        toggleOptionalFields.addEventListener('click', function() {
            optionalFields.style.display = (optionalFields.style.display === 'none' || !optionalFields.style.display) ? 'block' : 'none';
            this.textContent = (optionalFields.style.display === 'block') ? 'Hide Optional' : 'Show Optional';
        });
    }

    // Toggle nanotube indices based on crystal structure selection
    const crystalStructureSelect = document.getElementById('id_crystal_structure');
    const nanotubeIndicesContainer = document.getElementById('nanotube_indices_container');
    if (crystalStructureSelect && nanotubeIndicesContainer) {
        function toggleNanotubeIndicesDisplay() {
            if (crystalStructureSelect.value === 'CNT') {
                nanotubeIndicesContainer.style.display = 'block';
            } else {
                nanotubeIndicesContainer.style.display = 'none';
                document.getElementById('id_nanotube_indices').value = '';
            }
        }
        toggleNanotubeIndicesDisplay();
        crystalStructureSelect.addEventListener('change', toggleNanotubeIndicesDisplay);
    }
    
    
    // Initialize toggles for collapsible sections
    ['Dimensions', 'MeshOptions', 'Misc', 'Parallelization'].forEach(function(section) {

        const buttonId = 'toggle' + section;
        const button = document.getElementById('toggle' + section);
        const content = document.getElementById(section.toLowerCase() + 'Fields');
        if (button && content) {
            button.addEventListener('click', function() {
                content.style.display = (content.style.display === 'none' || !content.style.display) ? 'block' : 'none';
                button.innerText = (content.style.display === 'block') ? `Hide ${section}` : `Show ${section}`;
            });
        }
    });
});