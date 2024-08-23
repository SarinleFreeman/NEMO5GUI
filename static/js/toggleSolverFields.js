document.addEventListener('DOMContentLoaded', function() {
    const solverTypeSelector = document.getElementById('solverType');

    function toggleSolverFields() {
        const type = solverTypeSelector.value;
        const allFields = document.querySelectorAll('.solver-type-fields');
        allFields.forEach(field => field.style.display = 'none');

        if (type === 'NonlinearPoissonFEM') {
            document.getElementById('nonlinearFields').style.display = 'block';
        } else if (type === 'EMSchrodingerFEM') {
            document.getElementById('schrodingerFields').style.display = 'block';
        } else if (type === 'SemiclassicalFEM') {
            document.getElementById('semiclassicalFields').style.display = 'block';
        }
    }

    solverTypeSelector.addEventListener('change', toggleSolverFields);
    toggleSolverFields(); // Run on page load to set initial state
});