from django.db import models
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator


DISORDER_TYPE_CHOICES = [
    ("NonlinearPoissonFEM", "NonlinearPoissonFEM"),
    ("EMSchrodingerFEM", "EMSchrodingerFEM"),
    ("SemiclassicalFEM", "SemiclassicalFEM")
]

SPECTRUM_POSITIONS = [
        ('smallest_magnitude', 'Smallest Magnitude'),
        ('largest_magnitude', 'Largest Magnitude'),
        ('largest_real', 'Largest Real'),
        ('smallest_real', 'Smallest Real'),
        ('largest_imaginary', 'Largest Imaginary'),
        ('smallest_imaginary', 'Smallest Imaginary'),
    ]

EIGENSOLVER_CHOICES = [
        ('lanczos', 'Lanczos'),
        ('krylovschur', 'Krylov-Schur'),
        ('arnoldi', 'Arnoldi'),
        ('power', 'Power'),
        ('lapack', 'LAPACK'),
        ('subspace', 'Subspace'),
        ('arpack', 'ARPACK'),  # Include this only if ARPACK is compiled in SLEPc
        ('feast', 'FEAST'),    # Include this only if FEAST is available with MKL or compiled explicitly
        ('magma', 'MAGMA'),    # Include this only if MAGMA feature is enabled
        ('jd', 'JD'),          # Include this for libmesh version >= 0.9.5
        ('gd', 'GD')           # Include this for libmesh version >= 0.9.5
    ]

PC_TYPE_SCHRODINGER = [
    ('lu', 'LU Decomposition'),
    ('gamg', 'Geometric Algebraic Multigrid')
    ]

VALLEY_SPLITTING_OPTIONS_SCHRODINGER = [('gamma', 'Gamma (G)'),
                        ('x2', 'X2'),
                        ('x4', 'X4')]

class BaseSolverModel(models.Model):
    name = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=100, choices=DISORDER_TYPE_CHOICES)
    domain = models.ForeignKey('domains.Domain', on_delete=models.CASCADE)
    active_regions = models.ManyToManyField('regions.Region', blank=True)
    _disable_output = models.BooleanField(default=False)
    _search_flag = models.IntegerField(default=2)
    _trigger_flag = models.IntegerField(default=4)

    class Meta:
        abstract = True
        
class NonlinearPoissonFEM(BaseSolverModel):
    CB_initial_shift = models.FloatField(default=0.1)
    VB_initial_shift = models.FloatField(default=0.1)
    Dirichlet_nodes_output = models.BooleanField(default=False)
    Newton_step_only = models.BooleanField(default=False)
    disable_init = models.BooleanField(default=False)
    disable_output = models.BooleanField(default=False)
    disable_reinit = models.BooleanField(default=False)
    disable_reset_set = models.BooleanField(default=False)
    disable_solve = models.BooleanField(default=False)
    disable_step = models.BooleanField(default=False)
    init = models.TextField(default='', blank=True)
    output = models.TextField(default='', blank=True)
    reinit = models.TextField(default='', blank=True)
    solve = models.TextField(default='', blank=True)
    step = models.TextField(default='', blank=True)
    abs_tolerance = models.FloatField(default=1e-8, validators=[MinValueValidator(0)])
    atomistic_output = models.TextField(default='', blank=True)
    average_over_cell = models.BooleanField(default=True)
    boundary_condition = models.TextField(blank=True, null=True)
    boundary_regions = models.TextField(default='', blank=True)
    calculate_density_only = models.BooleanField(default=False)
    charge_model = models.CharField(max_length=50, default='electron_hole')
    chem_pot = models.FloatField(default=0.0)
    confined_band_solvers = models.TextField(default='', blank=True)
    constant_initial_potential = models.FloatField(default=0.0)
    copy_solution_from = models.CharField(max_length=100, blank=True, null=True)
    custom_convergence_test = models.BooleanField(default=False)
    density_solver = models.TextField(default='', blank=True)
    dependent_solvers = models.TextField(default='', blank=True)
    do_input_initial_nonlinearpoisson_potential = models.BooleanField(default=False)
    do_nonlinearpoisson_outputs_xyz_format = models.BooleanField(default=False)
    do_output_nonlinearpoisson_potential = models.BooleanField(default=False)
    do_output_potential_each_iteration = models.BooleanField(default=False)
    do_outputs_from_density_solver = models.BooleanField(default=False)
    equilibrium_el_chem_pot = models.FloatField(default=0.0)
    external_object_name = models.TextField(default='', blank=True)
    external_output = models.TextField(default='', blank=True)
    external_solver = models.CharField(max_length=100, blank=True, null=True)
    fem_output = models.CharField(max_length=100, blank=True, null=True)
    field = models.FloatField(default=0.0)
    friends = models.TextField(default='', blank=True)
    full_Newton_step = models.BooleanField(default=False)
    import_initial_potential_from_solver = models.BooleanField(default=False)
    import_on_FEM_grid = models.BooleanField(default=False)
    initial_potential_file_name = models.CharField(max_length=100, blank=True, null=True)
    initial_potential_point = models.CharField(max_length=100, blank=True, null=True)
    initial_potential_source = models.CharField(max_length=100, blank=True, null=True)
    interpolation_power = models.IntegerField(default=2)
    ksp_monitor = models.BooleanField(default=False)
    ksp_type = models.CharField(max_length=50, default='gmres')
    linear_solver_family = models.CharField(max_length=50, default='petsc')
    linear_solver_maxit = models.IntegerField(default=0)
    max_function_evals = models.IntegerField(default=1000)
    max_iterations = models.IntegerField(default=100, validators=[MinValueValidator(1)])
    max_nonlinear_step = models.FloatField(blank=True, null=True)
    node_potential_output = models.BooleanField(default=False)
    number_of_interpolation_points = models.IntegerField(default=4)
    number_of_output_points = models.IntegerField(default=100)
    one_dim_output = models.TextField(default='', blank=True)
    one_dim_output_average = models.BooleanField(default=True)
    output_at_each_iteration = models.BooleanField(default=False)
    output_dependent_solvers = models.TextField(default='', blank=True)
    output_file_suffix = models.CharField(max_length=100, blank=True, null=True)
    output_jacobian = models.BooleanField(default=False)
    output_line_corners = models.TextField(default='', blank=True)
    output_norms = models.BooleanField(default=False)
    output_residual = models.BooleanField(default=True)
    output_yz_integrated_density = models.BooleanField(default=True)
    pc_type = models.CharField(max_length=50, default='jacobi')
    petsc_solver_algorithm = models.CharField(max_length=50, default='ls')
    poisson_vtk_mesh = models.BooleanField(default=False)
    potential_at_initial_point = models.FloatField(default=0.0)
    rel_tolerance = models.FloatField(default=1e-6, validators=[MinValueValidator(0)])
    restart_data_input_file = models.CharField(max_length=100, blank=True, null=True)
    restart_data_output_file = models.CharField(max_length=100, blank=True, null=True)
    set_initial_field = models.BooleanField(default=False)
    set_initial_potential = models.BooleanField(default=True)
    shift_copied_solution_by_voltage = models.FloatField(default=0.0)
    solve_on_single_replica = models.BooleanField(default=False)
    solve_with_zero_density_first = models.BooleanField(default=False)
    step_abs_tolerance = models.FloatField(default=1e-10)
    step_rel_tolerance = models.FloatField(default=1e-10)
    stop_if_diverged = models.BooleanField(default=True)
    surface_of_regions = models.TextField(default='', blank=True)
    tic_toc_name = models.CharField(max_length=100, blank=True, null=True)
    tolerance_in_terms_of_doping = models.FloatField(default=0.0)
    use_average_density_as_a_guess = models.BooleanField(default=False)
    use_classical_jacobian = models.BooleanField(default=False)

    def __str__(self):
        
        return self.name
        
class EMSchrodingerFEM(BaseSolverModel):
    eigensolver = models.CharField(
        max_length=50,
        choices=EIGENSOLVER_CHOICES,
        default='krylovschur',
        help_text='Type of eigensolver to use.'
    )
    spectrum_position = models.CharField(
    max_length=50,
    choices=SPECTRUM_POSITIONS,
    default='smallest_magnitude',
    help_text='Position in the spectrum for which eigenvalues are sought.'
    )
    number_of_eigenvalues = models.IntegerField(default=5, validators=[MinValueValidator(1)], help_text='Number of eigenvalues to compute.')
    max_linear_solver_iterations = models.IntegerField(default=3000, validators=[MinValueValidator(1)], help_text='Maximum number of iterations for the linear solver.')
    linear_solver_tolerance = models.FloatField(default=1e-12, validators=[MinValueValidator(0)], help_text='Tolerance for the linear solver.')
    potential_solver = models.CharField(max_length=100, help_text='Solver to use for the potential field.')
    temperature = models.FloatField(default=1, validators=[MinValueValidator(0)], help_text='Simulation temperature.')
    chemical_potential = models.FloatField(default=0.64, help_text='Chemical potential.')
    B_field = models.FloatField(default=0, help_text='External magnetic field strength.')
    g_factor = models.FloatField(default=0, help_text='g-factor for the material.')
    finite_element_family = models.CharField(max_length=50, default='lagrange', help_text='Finite element family used in the simulation.')
    finite_element_order = models.IntegerField(default=1, validators=[MinValueValidator(1)], help_text='Order of the finite elements used.')
    FEM_integration_order = models.IntegerField(default=3, validators=[MinValueValidator(1)], help_text='Integration order for the finite element method.')
    use_density_interpolation = models.BooleanField(default=False, help_text='Whether to use density interpolation in the simulation.')
    integrate_density = models.BooleanField(default=True, help_text='Whether to integrate the density in the simulation.')
    use_exchange_potential = models.BooleanField(default=False, help_text='Whether to use exchange potential.')
    use_multiple_variables_for_spin_valley = models.BooleanField(default=False, help_text='Whether to use multiple variables for spin and valley.')
    max_refinement_iterations = models.IntegerField(default=0, validators=[MinValueValidator(0)], help_text='Maximum number of refinement iterations.')
    max_refinement_level = models.IntegerField(default=5, validators=[MinValueValidator(0)], help_text='Maximum level of mesh refinement.')
    refine_fraction = models.FloatField(default=0.9, validators=[MinValueValidator(0), MaxValueValidator(1)], help_text='Fraction of elements to refine.')
    coarsen_fraction = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1)], help_text='Fraction of elements to coarsen.')
    print_energy_levels = models.BooleanField(default=True, help_text='Whether to print energy levels.')
    print_num_electrons_under_Ef = models.BooleanField(default=True, help_text='Whether to print the number of electrons under the Fermi energy.')
    output_file_suffix = models.CharField(max_length=100, blank=True, help_text='Suffix for output files.')
    ksp_type = models.CharField(max_length=50, default='preonly', help_text='Type of Krylov subspace solver to use.')
    pc_type = models.CharField(
        max_length=50,
        choices=PC_TYPE_SCHRODINGER,
        default='lu',
        help_text='Type of eigenpreconditionersolver to use.'
    )
    linear_solver_family = models.CharField(max_length=50, default='mumps', help_text='Family of linear solvers to use.')
    tolerance = models.FloatField(default=1e-12, validators=[MinValueValidator(0)], help_text='Tolerance for computations.')
    valley = models.CharField(max_length=50, default='gamma', help_text='Valley type.')
    valley_degeneracy = models.IntegerField(default=-1, help_text='Degeneracy of the valley.')
    valley_splitting = models.FloatField(default=0, help_text='Energy splitting between valleys.')
    ll_width_to_splitting_ratio = models.FloatField(default=0.05, help_text='Ratio of Landau level width to valley splitting.')
    longitudinal_effective_mass_direction = models.CharField(max_length=1, default='X', help_text='Direction of longitudinal effective mass.')
    quadrature_rule = models.CharField(max_length=50, default='gauss', help_text='Quadrature rule used for numerical integration.')

    number_of_basis_vectors = models.IntegerField(default=20, validators=[MinValueValidator(1)], help_text='Number of basis vectors to use.')
    predictor_type = models.CharField(max_length=50, blank=True, help_text='Type of predictor to use.')
    density_integration_regions = models.TextField(blank=True, help_text='Regions for density integration.')
    fem_output = models.TextField(default='eigen_energies', help_text='Output options for FEM calculations.')
    eigen_vector_output_points_file = models.CharField(max_length=255, blank=True, help_text='File containing points for eigenvector output.')
    orthogonalize_interpolated_eigenvectors = models.BooleanField(default=False, help_text='Whether to orthogonalize interpolated eigenvectors.')
    eigen_vectors_interpolated_points_shift = models.CharField(max_length=100, blank=True, help_text='Shift for interpolated eigenvector points.')
    approx_module = models.CharField(max_length=100, blank=True, help_text='Approximation module to use.')
    potential_type = models.CharField(max_length=50, default='from_poisson', help_text='Type of potential to use.')
    tic_toc_name = models.CharField(max_length=100, default='schroFEM', help_text='Name for timing measurements.')

    d1_domain = models.CharField(max_length=100, blank=True, help_text='1D domain for approximation.')
    d2_domain = models.CharField(max_length=100, blank=True, help_text='2D domain for approximation.')
    d1_eigensolver = models.CharField(max_length=50, blank=True, help_text='Eigensolver for 1D approximation.')
    output_line_corners = models.TextField(blank=True, help_text='Corners of the output line for subband energies.')
    number_of_output_points = models.IntegerField(null=True, blank=True, help_text='Number of output points for subband energies.')

    def __str__(self):
        return self.name
 
    
class SemiclassicalFEM(BaseSolverModel):
    dimension = models.IntegerField(default=3)
    electron_chem_pot = models.FloatField(default=0.64)
    electron_temperature = models.FloatField(default=1)
    hole_chem_pot = models.FloatField(default=100)
    hole_temperature = models.FloatField(default=1)
    output_file_suffix = models.CharField(max_length=100, blank=True)
    param_type = models.CharField(max_length=100, default='NEMO5')
    tic_toc_name = models.CharField(max_length=100, default='full_semicl')

    def __str__(self):
        return self.name
    
