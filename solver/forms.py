from django import forms

from domains.models import Domain
from regions.models import Region
from .models import NonlinearPoissonFEM, EMSchrodingerFEM, SemiclassicalFEM, DISORDER_TYPE_CHOICES,VALLEY_SPLITTING_OPTIONS_SCHRODINGER

from django import forms

from django.apps import apps

class NonlinearPoissonFEMForm(forms.ModelForm):
    class Meta:
        model = NonlinearPoissonFEM
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Domain = apps.get_model('domains', 'Domain')
        Region = apps.get_model('regions', 'Region')
        
        self.fields['domain'] = forms.ModelChoiceField(
            queryset=Domain.objects.all(),
            empty_label="Select a domain",
            widget=forms.Select(attrs={'class': 'form-control'})
        )
        
        self.fields['active_regions'] = forms.ModelMultipleChoiceField(
            queryset=Region.objects.all().order_by('region_number'),
            widget=forms.CheckboxSelectMultiple,
            required=False
        )
        widgets = {
            'name': forms.TextInput(attrs={'required': True, 'placeholder': 'A unique name tag / identifier for this solver instance'}),
            'type': forms.Select(choices=[('NonlinearPoissonFEM', 'NonlinearPoissonFEM')], attrs={'disabled': 'disabled'}),
            '_disable_output': forms.CheckboxInput(),
            '_search_flag': forms.NumberInput(attrs={'min': 0, 'max': 10}),
            '_trigger_flag': forms.NumberInput(attrs={'min': 0, 'max': 10}),
            'CB_initial_shift': forms.NumberInput(attrs={'step': 0.1, 'placeholder': 'Initial shift for conduction band (eV)'}),
            'VB_initial_shift': forms.NumberInput(attrs={'step': 0.1, 'placeholder': 'Initial shift for valence band (eV)'}),
            'Dirichlet_nodes_output': forms.CheckboxInput(),
            'Newton_step_only': forms.CheckboxInput(),
            'disable_init': forms.CheckboxInput(),
            'disable_output': forms.CheckboxInput(),
            'disable_reinit': forms.CheckboxInput(),
            'disable_reset_set': forms.CheckboxInput(),
            'disable_solve': forms.CheckboxInput(),
            'disable_step': forms.CheckboxInput(),
            'init': forms.Textarea(attrs={'rows': 3, 'placeholder': 'List of solvers to trigger init command'}),
            'output': forms.Textarea(attrs={'rows': 3, 'placeholder': 'List of solvers to trigger output command'}),
            'reinit': forms.Textarea(attrs={'rows': 3, 'placeholder': 'List of solvers to trigger reinit command'}),
            'solve': forms.Textarea(attrs={'rows': 3, 'placeholder': 'List of solvers to trigger solve command'}),
            'step': forms.Textarea(attrs={'rows': 3, 'placeholder': 'List of solvers to trigger step command'}),
            'abs_tolerance': forms.NumberInput(attrs={'step': '1e-9', 'value': '1e-8', 'placeholder': 'Absolute tolerance of the residual'}),
            'atomistic_output': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Atom-based quantities to save (e.g., potential, charge, doping)'}),
            'average_over_cell': forms.CheckboxInput(),
            'boundary_condition': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Specify boundary conditions (type, name, regions, voltage, etc.)'}),
            'boundary_regions': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Regions for boundary conditions'}),
            'calculate_density_only': forms.CheckboxInput(),
            'charge_model': forms.Select(choices=[('electron_hole', 'Electron-Hole'), ('electron_core', 'Electron-Core')]),
            'chem_pot': forms.NumberInput(attrs={'step': 0.1, 'value': 0.0, 'placeholder': 'Chemical potential for Fermi distribution (eV)'}),
            'confined_band_solvers': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Names of band structure solvers for confinement'}),
            'constant_initial_potential': forms.NumberInput(attrs={'step': 0.1, 'placeholder': 'Initial potential guess (eV)'}),
            'copy_solution_from': forms.TextInput(attrs={'placeholder': 'Name of Poisson simulation to copy solution from'}),
            'custom_convergence_test': forms.CheckboxInput(),
            'density_solver': forms.TextInput(attrs={'placeholder': 'Names of solvers where charge can be found'}),
            'dependent_solvers': forms.Textarea(attrs={'rows': 3, 'placeholder': 'List of solvers dependent on this Poisson simulation'}),
            'do_input_initial_nonlinearpoisson_potential': forms.CheckboxInput(),
            'do_nonlinearpoisson_outputs_xyz_format': forms.CheckboxInput(),
            'do_output_nonlinearpoisson_potential': forms.CheckboxInput(),
            'do_output_potential_each_iteration': forms.CheckboxInput(),
            'do_outputs_from_density_solver': forms.CheckboxInput(),
            'equilibrium_el_chem_pot': forms.NumberInput(attrs={'step': 0.1, 'placeholder': 'Equilibrium electron chemical potential (eV)'}),
            'external_object_name': forms.TextInput(attrs={'placeholder': 'Name of external object to set as incomplete'}),
            'external_output': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Names of external solvers for output'}),
            'external_solver': forms.TextInput(attrs={'placeholder': 'Name of external solver to set job as incomplete'}),
            'fem_output': forms.TextInput(attrs={'placeholder': 'FEM output type (e.g., free_charge_cm-3)'}),
            'field': forms.NumberInput(attrs={'step': 0.1, 'placeholder': 'Electric field value'}),
            'friends': forms.Textarea(attrs={'rows': 3, 'placeholder': 'List of friend solvers to ask for potential'}),
            'full_Newton_step': forms.CheckboxInput(),
            'import_initial_potential_from_solver': forms.CheckboxInput(),
            'import_on_FEM_grid': forms.CheckboxInput(),
            'initial_potential_file_name': forms.TextInput(attrs={'placeholder': 'Filename for initial potential'}),
            'initial_potential_point': forms.TextInput(attrs={'placeholder': 'Initial potential point, e.g., 0,0,0'}),
            'initial_potential_source': forms.TextInput(attrs={'placeholder': 'Name of solver to import initial potential from'}),
            'interpolation_power': forms.NumberInput(attrs={'min': 1, 'max': 10, 'placeholder': 'Power for distance weight in charge density interpolation'}),
            'ksp_monitor': forms.CheckboxInput(),
            'ksp_type': forms.Select(choices=[('gmres', 'GMRES'), ('bcgs', 'BiCGSTAB')]),
            'linear_solver_family': forms.Select(choices=[('petsc', 'PETSc'), ('mumps', 'MUMPS')]),
            'linear_solver_maxit': forms.NumberInput(attrs={'min': 0, 'placeholder': 'Max iterations for iterative linear solver'}),
            'max_function_evals': forms.NumberInput(attrs={'min': 1, 'value': 1000, 'placeholder': 'Max Newton right-hand-side evaluations'}),
            'max_iterations': forms.NumberInput(attrs={'min': 1, 'value': 100, 'placeholder': 'Maximum number of Newton iterations'}),
            'max_nonlinear_step': forms.NumberInput(attrs={'step': 0.1, 'placeholder': 'Maximum value of a step in Non-linear solver'}),
            'node_potential_output': forms.CheckboxInput(),
            'number_of_interpolation_points': forms.NumberInput(attrs={'min': 1, 'value': 4, 'placeholder': 'Number of surrounding points for charge density interpolation'}),
            'number_of_output_points': forms.NumberInput(attrs={'min': 1, 'value': 100, 'placeholder': 'Number of points for 1D line plotting'}),
            'one_dim_output': forms.Textarea(attrs={'rows': 3, 'placeholder': '1D output quantities (e.g., potential, free_charge_cm-3)'}),
            'one_dim_output_average': forms.CheckboxInput(),
            'output_at_each_iteration': forms.CheckboxInput(),
            'output_dependent_solvers': forms.Textarea(attrs={'rows': 3, 'placeholder': 'List of dependent solvers for output'}),
            'output_file_suffix': forms.TextInput(attrs={'placeholder': 'Suffix for output files'}),
            'output_jacobian': forms.CheckboxInput(),
            'output_line_corners': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Line corners for 1D output, e.g., [x1,y1,z1],[x2,y2,z2]'}),
            'output_norms': forms.CheckboxInput(),
            'output_residual': forms.CheckboxInput(),
            'output_yz_integrated_density': forms.CheckboxInput(),
            'pc_type': forms.Select(choices=[('asm', 'ASM'), ('lu', 'LU'), ('jacobi', 'Jacobi')]),
            'petsc_solver_algorithm': forms.Select(choices=[('ls', 'Line Search'), ('tr', 'Trust Region')]),
            'poisson_vtk_mesh': forms.CheckboxInput(),
            'potential_at_initial_point': forms.NumberInput(attrs={'step': 0.1, 'placeholder': 'Potential at initial point (eV)'}),
            'rel_tolerance': forms.NumberInput(attrs={'step': '1e-7', 'value': '1e-6', 'placeholder': 'Relative residual tolerance of Newton solver'}),
            'restart_data_input_file': forms.TextInput(attrs={'placeholder': 'File for restarting simulation'}),
            'restart_data_output_file': forms.TextInput(attrs={'placeholder': 'File to save restart data'}),
            'set_initial_field': forms.CheckboxInput(),
            'set_initial_potential': forms.CheckboxInput(),
            'shift_copied_solution_by_voltage': forms.NumberInput(attrs={'step': 0.1, 'placeholder': 'Voltage shift for copied Poisson solution'}),
            'solve_on_single_replica': forms.CheckboxInput(),
            'solve_with_zero_density_first': forms.CheckboxInput(),
            'step_abs_tolerance': forms.NumberInput(attrs={'step': '1e-11', 'value': '1e-10', 'placeholder': 'Absolute step tolerance of Newton solver'}),
            'step_rel_tolerance': forms.NumberInput(attrs={'step': '1e-11', 'value': '1e-10', 'placeholder': 'Relative step tolerance of Newton solver'}),
            'stop_if_diverged': forms.CheckboxInput(),
            'surface_of_regions': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Surface regions for boundary conditions'}),
            'tic_toc_name': forms.TextInput(attrs={'placeholder': 'Prefix for tic-tocs'}),
            'tolerance_in_terms_of_doping': forms.NumberInput(attrs={'step': '1e-5', 'placeholder': 'Tolerance relative to doping'}),
            'use_average_density_as_a_guess': forms.CheckboxInput(),
            'use_classical_jacobian': forms.CheckboxInput(),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].initial = "NonlinearPoissonFEM"
        self.fields['type'].disabled = True

        self.fields['name'].help_text = "A unique name tag / identifier for this specific instance of the NonlinearPoissonFEM solver."
        self.fields['_search_flag'].help_text = "Flag command to search nested solver."
        self.fields['_trigger_flag'].help_text = "Flag command for nested execution of solvers."
        self.fields['_disable_output'].help_text = "Flag command to disable solver output execution."
        self.fields['Dirichlet_nodes_output'].help_text = "If checked, outputs actual potential at Dirichlet nodes (e.g. gate)."
        self.fields['Newton_step_only'].help_text = "If checked, only a single step rather than the full self-consistent iteration is performed."
        self.fields['disable_init'].help_text = "If checked, disables initialization."
        self.fields['disable_output'].help_text = "If checked, disables solver output execution."
        self.fields['disable_reinit'].help_text = "If checked, disables re-initialization."
        self.fields['disable_reset_set'].help_text = "If checked, disables re-initialization of sets."
        self.fields['disable_solve'].help_text = "If checked, disables solver solution."
        self.fields['disable_step'].help_text = "If checked, disables change of sets when iterators are defined."
        self.fields['average_over_cell'].help_text = "If checked, averages quantities over the cell. Leave this one true (default)."
        self.fields['calculate_density_only'].help_text = "If checked, calculates the density for a constant potential."
        self.fields['custom_convergence_test'].help_text = "If checked, uses a custom Poisson/transport solver convergence test."
        self.fields['do_input_initial_nonlinearpoisson_potential'].help_text = "If checked, inputs initial nonlinear Poisson potential."
        self.fields['do_nonlinearpoisson_outputs_xyz_format'].help_text = "If checked, output will be done in the cartesian XYZ format."
        self.fields['do_output_nonlinearpoisson_potential'].help_text = "If checked, outputs the potential in a separate file in FEM format at the end of NonlinearPoisson."
        self.fields['do_output_potential_each_iteration'].help_text = "If checked, outputs the potential in a separate file in FEM format on each Schrodinger solve."
        self.fields['do_outputs_from_density_solver'].help_text = "If checked, enables outputs specified in density quantum solver at the end of the NonlinearPoisson solution."
        self.fields['full_Newton_step'].help_text = "If checked, uses full Newton step for search in Newton solver."
        self.fields['import_initial_potential_from_solver'].help_text = "If checked, imports initial potential from another solver."
        self.fields['import_on_FEM_grid'].help_text = "If checked, imports initial potential on FEM grid (not atomic)."
        self.fields['ksp_monitor'].help_text = "If checked, enables a monitor for Krylov Sub-sPace solver in PETSc package."
        self.fields['node_potential_output'].help_text = "If checked, writes the potential to (sim-name)_nodal_potential.dat."
        self.fields['one_dim_output_average'].help_text = "If checked, uses unit cells for 1D discretization and performs averaging within cells."
        self.fields['output_at_each_iteration'].help_text = "If checked, outputs the potential in a separate file in FEM format on each Schrodinger solve."
        self.fields['output_jacobian'].help_text = "If checked, outputs the Jacobian of Non-linear solver."
        self.fields['output_norms'].help_text = "If checked, prints the norms as a function of iteration. Useful for debugging."
        self.fields['output_residual'].help_text = "If checked, outputs the residual of Non-linear solver."
        self.fields['output_yz_integrated_density'].help_text = "If checked, outputs density along x direction, integrated on xy planes."
        self.fields['poisson_vtk_mesh'].help_text = "If checked, saves the electrostatic potential in VTK format on a tetrahedral mesh."
        self.fields['set_initial_field'].help_text = "If checked, sets a constant electric field at the beginning."
        self.fields['set_initial_potential'].help_text = "If checked, sets an initial potential (read from file or computed)."
        self.fields['solve_on_single_replica'].help_text = "If checked, solves Non-linear Poisson on a single replica of the geometry."
        self.fields['solve_with_zero_density_first'].help_text = "If checked, solves potential with zero density everywhere first."
        self.fields['stop_if_diverged'].help_text = "If checked, stops the self-consistent loop if potential doesn't converge."
        self.fields['use_average_density_as_a_guess'].help_text = "If checked, uses average density as an initial guess. (Note: Must be false, true has a bug)"
        self.fields['use_classical_jacobian'].help_text = "If checked, calculates the Jacobian using the semiclassical charge density with spatially dependent Fermi level."


class EMSchrodingerFEMForm(forms.ModelForm):
    class Meta:
        model = EMSchrodingerFEM
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'required': True, 'placeholder': 'Enter solver name', 'id': 'id_name'}),
            'type': forms.TextInput(attrs={'required': True, 'value': 'EMSchrodingerFEM', 'readonly': True}),
            'eigensolver': forms.Select(attrs={'placeholder': 'Enter eigensolver', 'id': 'id_eigensolver'}),
            'spectrum_position': forms.Select(attrs={'placeholder': 'Enter spectrum position', 'id': 'id_spectrum_position'}),
            'number_of_eigenvalues': forms.NumberInput(attrs={'min': 1, 'placeholder': 'Enter number of eigenvalues', 'id': 'id_number_of_eigenvalues'}),
            'max_linear_solver_iterations': forms.NumberInput(attrs={'min': 1, 'placeholder': 'Enter max linear solver iterations', 'id': 'id_max_linear_solver_iterations'}),
            'linear_solver_tolerance': forms.NumberInput(attrs={'step': 'any', 'placeholder': 'Enter linear solver tolerance', 'id': 'id_linear_solver_tolerance'}),
            'potential_solver': forms.TextInput(attrs={'placeholder': 'Enter potential solver', 'id': 'id_potential_solver'}),
            'temperature': forms.NumberInput(attrs={'min': 0, 'step': 'any', 'placeholder': 'Enter temperature', 'id': 'id_temperature'}),
            'chemical_potential': forms.NumberInput(attrs={'step': 'any', 'placeholder': 'Enter chemical potential', 'id': 'id_chemical_potential'}),
            'B_field': forms.NumberInput(attrs={'step': 'any', 'placeholder': 'Enter B field', 'id': 'id_B_field'}),
            'g_factor': forms.NumberInput(attrs={'step': 'any', 'placeholder': 'Enter g factor', 'id': 'id_g_factor'}),
            'finite_element_family': forms.Select(choices=[
        ('lagrange', 'Lagrange'),
        ('hierarchic', 'Hierarchic'),
        ('hermite', 'Hermite')
    ],attrs={'placeholder': 'Enter finite element family', 'id': 'id_finite_element_family'}),
            'finite_element_order': forms.NumberInput(attrs={'min': 1, 'placeholder': 'Enter finite element order', 'id': 'id_finite_element_order'}),
            'FEM_integration_order': forms.NumberInput(attrs={'min': 1, 'placeholder': 'Enter FEM integration order', 'id': 'id_FEM_integration_order'}),
            'use_density_interpolation': forms.CheckboxInput(attrs={'id': 'id_use_density_interpolation'}),
            'integrate_density': forms.CheckboxInput(attrs={'id': 'id_integrate_density'}),
            'use_exchange_potential': forms.CheckboxInput(attrs={'id': 'id_use_exchange_potential'}),
            'use_multiple_variables_for_spin_valley': forms.CheckboxInput(attrs={'id': 'id_use_multiple_variables_for_spin_valley'}),
            'max_refinement_iterations': forms.NumberInput(attrs={'min': 0, 'placeholder': 'Enter max refinement iterations', 'id': 'id_max_refinement_iterations'}),
            'max_refinement_level': forms.NumberInput(attrs={'min': 0, 'placeholder': 'Enter max refinement level', 'id': 'id_max_refinement_level'}),
            'refine_fraction': forms.NumberInput(attrs={'min': 0, 'max': 1, 'step': 'any', 'placeholder': 'Enter refine fraction', 'id': 'id_refine_fraction'}),
            'coarsen_fraction': forms.NumberInput(attrs={'min': 0, 'max': 1, 'step': 'any', 'placeholder': 'Enter coarsen fraction', 'id': 'id_coarsen_fraction'}),
            'print_energy_levels': forms.CheckboxInput(attrs={'id': 'id_print_energy_levels'}),
            'print_num_electrons_under_Ef': forms.CheckboxInput(attrs={'id': 'id_print_num_electrons_under_Ef'}),
            'output_file_suffix': forms.TextInput(attrs={'placeholder': 'Enter output file suffix', 'id': 'id_output_file_suffix'}),
            'ksp_type': forms.TextInput(attrs={'placeholder': 'Enter ksp type', 'id': 'id_ksp_type'}),
            'pc_type': forms.Select(attrs={'placeholder': 'Enter pc type', 'id': 'id_pc_type'}),
            'linear_solver_family': forms.Select(choices=[('petsc', 'PETSc'), ('mumps', 'MUMPS')], attrs={'placeholder': 'Enter linear solver family', 'id': 'id_linear_solver_family'}),
            'tolerance': forms.NumberInput(attrs={'step': 'any', 'placeholder': 'Enter tolerance', 'id': 'id_tolerance'}),
            'valley': forms.Select(
                    choices=VALLEY_SPLITTING_OPTIONS_SCHRODINGER,
                    attrs={'id': 'id_valley','placeholder': 'Enter valley'}
                ),
            'valley_splitting': forms.NumberInput(attrs={'step': 'any', 'placeholder': 'Enter valley splitting', 'id': 'id_valley_splitting'}),
            'll_width_to_splitting_ratio': forms.NumberInput(attrs={'step': 'any', 'placeholder': 'Enter ll width to splitting ratio', 'id': 'id_ll_width_to_splitting_ratio'}),
            'longitudinal_effective_mass_direction': forms.Select(
                choices=[
                    ('X', 'X-axis'),
                    ('Y', 'Y-axis'),
                    ('Z', 'Z-axis')
                ],
                attrs={'id': 'id_longitudinal_effective_mass_direction', 'placeholder': 'Select mass direction'}
            ),
            'quadrature_rule': forms.Select(
                choices=[
                    ('gauss', 'Gauss'),
                    ('trapezoidal', 'Trapezoidal')
                ],
                attrs={'id': 'id_quadrature_rule', 'placeholder': 'Select quadrature rule'}
            ),
            # New fields
            'number_of_basis_vectors': forms.NumberInput(attrs={'min': 1, 'placeholder': 'Enter number of basis vectors', 'id': 'id_number_of_basis_vectors'}),
            'predictor_type': forms.TextInput(attrs={'placeholder': 'Enter predictor type', 'id': 'id_predictor_type'}),
            'density_integration_regions': forms.TextInput(attrs={'placeholder': 'Enter density integration regions', 'id': 'id_density_integration_regions'}),
            'fem_output': forms.TextInput(attrs={'placeholder': 'Enter FEM output options', 'id': 'id_fem_output'}),
            'eigen_vector_output_points_file': forms.TextInput(attrs={'placeholder': 'Enter eigenvector output points file', 'id': 'id_eigen_vector_output_points_file'}),
            'orthogonalize_interpolated_eigenvectors': forms.CheckboxInput(attrs={'id': 'id_orthogonalize_interpolated_eigenvectors'}),
            'eigen_vectors_interpolated_points_shift': forms.TextInput(attrs={'placeholder': 'Enter eigenvector interpolated points shift', 'id': 'id_eigen_vectors_interpolated_points_shift'}),
            'approx_module': forms.TextInput(attrs={'placeholder': 'Enter approximation module', 'id': 'id_approx_module'}),
            'potential_type': forms.TextInput(attrs={'placeholder': 'Enter potential type', 'id': 'id_potential_type'}),
            'tic_toc_name': forms.TextInput(attrs={'placeholder': 'Enter tic toc name', 'id': 'id_tic_toc_name'}),
            'd1_domain': forms.TextInput(attrs={'placeholder': 'Enter 1D domain', 'id': 'id_d1_domain'}),
            'd2_domain': forms.TextInput(attrs={'placeholder': 'Enter 2D domain', 'id': 'id_d2_domain'}),
            'd1_eigensolver': forms.TextInput(attrs={'placeholder': 'Enter 1D eigensolver', 'id': 'id_d1_eigensolver'}),
            'output_line_corners': forms.TextInput(attrs={'placeholder': 'Enter output line corners', 'id': 'id_output_line_corners'}),
            'number_of_output_points': forms.NumberInput(attrs={'min': 1, 'placeholder': 'Enter number of output points', 'id': 'id_number_of_output_points'}),
            '_disable_output': forms.CheckboxInput(attrs={'id': 'id_disable_output'}),
            '_search_flag': forms.NumberInput(attrs={'placeholder': 'Enter search flag', 'id': 'id_search_flag'}),
            '_trigger_flag': forms.NumberInput(attrs={'placeholder': 'Enter trigger flag', 'id': 'id_trigger_flag'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

                
        self.fields['domain'] = forms.ModelChoiceField(
            queryset=Domain.objects.all(),
            empty_label="Select a domain",
            widget=forms.Select(attrs={'class': 'form-control'})
        )
        
        self.fields['active_regions'] = forms.ModelMultipleChoiceField(
            queryset=Region.objects.all().order_by('region_number'),
            widget=forms.CheckboxSelectMultiple,
            required=False
        )

        self.fields['fem_output'].initial = [
            'charge_density',
            'eigen_vectors',
            'eigen_vectors_along_a_line',
            'eigen_vectors_interpolated_at_points',
            'eigen_energies'
        ]
        self.fields['eigen_vectors_interpolated_points_shift'].initial = '(0,0,0)'
        self.fields['eigen_vectors_interpolated_points_shift'].initial ="[ [x1, y1, z1],[x2, y2, z2], [x3, y3, z3]]"

        self.fields['type'].initial = 'EMSchrodingerFEM'
        self.fields['type'].disabled = True

        self.fields['ksp_type'].initial = 'pre_only'
        self.fields['ksp_type'].disabled = True

        self.fields['pc_type'].label = "Preconditioner Type"
        self.fields['name'].label = "Solver Name"
        self.fields['type'].label = "Solver Type"
        self.fields['domain'].label = "Simulation Domain"
        self.fields['active_regions'].label = "Active Regions (e.g., 1,2,3)"
        self.fields['eigensolver'].label = "Eigensolver Type"
        self.fields['spectrum_position'].label = "Spectrum Position"
        self.fields['number_of_eigenvalues'].label = "Number of Eigenvalues"
        self.fields['max_linear_solver_iterations'].label = "Maximum Linear Solver Iterations"
        self.fields['linear_solver_tolerance'].label = "Linear Solver Tolerance"
        self.fields['potential_solver'].label = "Potential Solver"
        self.fields['temperature'].label = "Temperature (K)"
        self.fields['chemical_potential'].label = "Chemical Potential"
        self.fields['B_field'].label = "Magnetic Field (B)"
        self.fields['g_factor'].label = "g-Factor"
        self.fields['finite_element_family'].label = "Finite Element Family"
        self.fields['finite_element_order'].label = "Finite Element Order"
        self.fields['FEM_integration_order'].label = "FEM Integration Order"
        self.fields['use_density_interpolation'].label = "Use Density Interpolation"
        self.fields['integrate_density'].label = "Integrate Density"
        self.fields['use_exchange_potential'].label = "Use Exchange Potential"
        self.fields['use_multiple_variables_for_spin_valley'].label = "Use Multiple Variables for Spin-Valley"
        self.fields['max_refinement_iterations'].label = "Maximum Refinement Iterations"
        self.fields['max_refinement_level'].label = "Maximum Refinement Level"
        self.fields['refine_fraction'].label = "Refinement Fraction"
        self.fields['coarsen_fraction'].label = "Coarsening Fraction"
        self.fields['print_energy_levels'].label = "Print Energy Levels"
        self.fields['print_num_electrons_under_Ef'].label = "Print Number of Electrons under Fermi Level"
        self.fields['output_file_suffix'].label = "Output File Suffix"
        self.fields['ksp_type'].label = "KSP Type"
        self.fields['linear_solver_family'].label = "Linear Solver Family"
        self.fields['tolerance'].label = "Solver Tolerance"
        self.fields['valley'].label = "Valley"
        self.fields['valley_splitting'].label = "Valley Splitting"
        self.fields['ll_width_to_splitting_ratio'].label = "Landau Level Width to Splitting Ratio"
        self.fields['longitudinal_effective_mass_direction'].label = "Longitudinal Effective Mass Direction"
        self.fields['quadrature_rule'].label = "Quadrature Rule"
        self.fields['number_of_basis_vectors'].label = "Number of Basis Vectors"
        self.fields['predictor_type'].label = "Predictor Type"
        self.fields['density_integration_regions'].label = "Density Integration Regions"
        self.fields['fem_output'].label = "FEM Output Options"
        self.fields['eigen_vector_output_points_file'].label = "Eigenvector Output Points File"
        self.fields['orthogonalize_interpolated_eigenvectors'].label = "Orthogonalize Interpolated Eigenvectors"
        self.fields['eigen_vectors_interpolated_points_shift'].label = "Eigenvector Interpolated Points Shift"
        self.fields['approx_module'].label = "Approximation Module"
        self.fields['potential_type'].label = "Potential Type"
        self.fields['tic_toc_name'].label = "Tic Toc Name"
        self.fields['d1_domain'].label = "1D Domain"
        self.fields['d2_domain'].label = "2D Domain"
        self.fields['d1_eigensolver'].label = "1D Eigensolver"
        self.fields['output_line_corners'].label = "Output Line Corners"
        self.fields['number_of_output_points'].label = "Number of Output Points"
        self.fields['_disable_output'].label = "Disable Output"
        self.fields['_search_flag'].label = "Search Flag"
        self.fields['_trigger_flag'].label = "Trigger Flag"

        # Add help_text to checkbox fields
        checkbox_fields = [
            'use_density_interpolation', 'integrate_density', 'use_exchange_potential',
            'use_multiple_variables_for_spin_valley', 'print_energy_levels',
            'print_num_electrons_under_Ef', 'orthogonalize_interpolated_eigenvectors',
            '_disable_output'
        ]
        for field in checkbox_fields:
            self.fields[field].widget.attrs['title'] = self.fields[field].help_text


class SemiclassicalFEMForm(forms.ModelForm):
    class Meta:
        model = SemiclassicalFEM
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'required': True, 'placeholder': 'Enter solver name', 'id': 'id_name'}),
            'type': forms.Select(attrs={'required': True, 'id': 'id_type'}),
            'dimension': forms.NumberInput(attrs={'min': 1, 'placeholder': 'Enter dimension', 'id': 'id_dimension'}),
            'electron_chem_pot': forms.NumberInput(attrs={'step': 'any', 'placeholder': 'Enter electron chemical potential', 'id': 'id_electron_chem_pot'}),
            'electron_temperature': forms.NumberInput(attrs={'step': 'any', 'placeholder': 'Enter electron temperature', 'id': 'id_electron_temperature'}),
            'hole_chem_pot': forms.NumberInput(attrs={'step': 'any', 'placeholder': 'Enter hole chemical potential', 'id': 'id_hole_chem_pot'}),
            'hole_temperature': forms.NumberInput(attrs={'step': 'any', 'placeholder': 'Enter hole temperature', 'id': 'id_hole_temperature'}),
            'output_file_suffix': forms.TextInput(attrs={'placeholder': 'Enter output file suffix', 'id': 'id_output_file_suffix'}),
            'param_type': forms.TextInput(attrs={'placeholder': 'Enter parameter type', 'id': 'id_param_type'}),
            'tic_toc_name': forms.TextInput(attrs={'placeholder': 'Enter tic toc name', 'id': 'id_tic_toc_name'}),
            '_disable_output': forms.CheckboxInput(attrs={'id': 'id_disable_output'}),
            '_search_flag': forms.NumberInput(attrs={'min': 0, 'placeholder': 'Enter search flag', 'id': 'id_search_flag'}),
            '_trigger_flag': forms.NumberInput(attrs={'min': 0, 'placeholder': 'Enter trigger flag', 'id': 'id_trigger_flag'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

                
        self.fields['domain'] = forms.ModelChoiceField(
            queryset=Domain.objects.all(),
            empty_label="Select a domain",
            widget=forms.Select(attrs={'class': 'form-control'})
        )
        
        self.fields['active_regions'] = forms.ModelMultipleChoiceField(
            queryset=Region.objects.all().order_by('region_number'),
            widget=forms.CheckboxSelectMultiple,
            required=False
        )

        self.fields['type'].initial = 'SemiclassicalFEM'
        self.fields['type'].disabled = True
