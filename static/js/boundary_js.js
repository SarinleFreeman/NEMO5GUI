function showRelevantFields() {
    var conditionType = document.getElementById('id_type').value;
    var fields = document.querySelectorAll('[id^="div_id_"]');
    
    fields.forEach(function(field) {
        field.style.display = 'none';
    });

    // Fields that should always be visible
    document.getElementById('div_id_type').style.display = 'block';
    document.getElementById('div_id_name').style.display = 'block';
    document.getElementById('div_id_solver_name').style.display = 'block';

    if (conditionType === 'ElectrostaticContact') {
        document.getElementById('div_id_voltage').style.display = 'block';
        document.getElementById('div_id_boundary_regions').style.display = 'block';
        document.getElementById('div_id_single_surface_normal').style.display = 'block';
        document.getElementById('div_id_surface_of_regions').style.display = 'block';
    } else if (conditionType === 'PotentialFromSolver') {
        document.getElementById('div_id_potential_simulation').style.display = 'block';
    } else if (conditionType === 'NormalField') {
        document.getElementById('div_id_E_field').style.display = 'block';
    } else if (conditionType === 'SchottkyContact') {
        document.getElementById('div_id_semiconductor').style.display = 'block';
        document.getElementById('div_id_metal_work_function').style.display = 'block';
        document.getElementById('div_id_voltage').style.display = 'block';
    }
}

// Call the function on page load to set initial visibility
document.addEventListener('DOMContentLoaded', function() {
    showRelevantFields();
});