# views.py in your main app directory
from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
import json
from django.http import HttpResponse
from domains.models import Domain
from materials.models import Material
from regions.models import Region, BoundaryRegion
from solver.models import NonlinearPoissonFEM,EMSchrodingerFEM,SemiclassicalFEM
from boundary.models import BoundaryCondition

def home_view(request):
    return render(request, 'home.html')


def generate_input_deck(materials, domains, regions, nonlinear_poisson_solvers, em_schrodinger_solvers, semiclassical_solvers, boundary_conditions, boundary_regions):
    input_deck = "Structure {\n"
    for material in materials:
            input_deck += "  Material {\n"
            input_deck += f"    name = {material.name}\n"
            input_deck += f"    tag = {material.tag}\n"
            input_deck += f"    crystal_structure = {material.crystal_structure}\n"
            
            # Validate and format regions
            try:
                material_regions = [int(r.strip()) for r in material.regions.split(',')]
                input_deck += f"    regions = ({','.join(map(str, material_regions))})\n"
            except ValueError:
                input_deck += f"    # Error: Invalid regions format\n"
            
            if material.doping_type:
                input_deck += f"    doping_type = {material.doping_type}\n"
            if material.doping_density is not None:
                input_deck += f"    doping_density = {material.doping_density}\n"
            if material.charge_model:
                input_deck += f"    charge_model = {material.charge_model}\n"
            if material.doping_ionization_model:
                input_deck += f"    doping_ionization_model = {material.doping_ionization_model}\n"
            if material.doping_temperature is not None:
                input_deck += f"    doping_temperature = {material.doping_temperature}\n"
            if material.ionization_energy is not None:
                input_deck += f"    ionization_energy = {material.ionization_energy}\n"
            if material.doping_degeneracy is not None:
                input_deck += f"    doping_degeneracy = {material.doping_degeneracy}\n"
            if material.nanotube_indices:
                input_deck += f"    nanotube_indices = {material.nanotube_indices}\n"
            if material.disorder_type:
                input_deck += f"    disorder_type = {material.disorder_type}\n"
            if material.seed is not None:
                input_deck += f"    seed = {material.seed}\n"
            if material.polarization:
                input_deck += f"    polarization = {material.polarization}\n"
            if material.strain_simulation:
                input_deck += f"    strain_simulation = true\n"
            
            # Alloy-specific parameters
            if material.is_alloy:
                input_deck += f"    is_alloy = true\n"
                input_deck += f"    mole_fraction = {material.mole_fraction}\n"
            
            input_deck += "  }\n\n"
        
    # Domain
    for domain in domains:
        input_deck += "  Domain {\n"
        input_deck += f"    name = {domain.name}\n"
        input_deck += f"    type = {domain.domain_type}\n"
        
        # Handle regions with error checking
        try:
            domain_regions = [int(r.strip()) for r in domain.regions.split(',')]
            input_deck += f"    regions = ({','.join(map(str, domain_regions))})\n"
        except ValueError:
            input_deck += f"    # Error: Invalid regions format for {domain.name}\n"
        
        if domain.mesh_dimension != 3:
            input_deck += f"    mesh_dimension = {domain.mesh_dimension}\n"
        
        # Coordinates
        for coord in ['xmin', 'xmax', 'ymin', 'ymax', 'zmin', 'zmax']:
            value = getattr(domain, coord)
            if value is not None:
                input_deck += f"    {coord} = {value}\n"
        
        # Grid divisions and spacing
        for param in ['nx', 'ny', 'nz', 'dx', 'dy', 'dz']:
            value = getattr(domain, param)
            if value is not None:
                input_deck += f"    {param} = {value}\n"
        
        if domain.element_kind and domain.element_kind != "cuboid8":
            input_deck += f"    element_kind = {domain.element_kind}\n"
        if domain.import_from_file:
            input_deck += f"    import_from_file = {domain.import_from_file}\n"
        if domain.submesh_from_domain:
            input_deck += f"    submesh_from_domain = {domain.submesh_from_domain}\n"
        
        # Handle nonorthogonal mesh and vectors
        if domain.nonorthogonal_mesh:
            input_deck += f"    nonorthogonal_mesh = true\n"
            for i in range(1, 4):
                vector = getattr(domain, f'mesh_vector{i}')
                if vector:
                    try:
                        vector_values = [float(v.strip()) for v in vector.split(',')]
                        if len(vector_values) == 3:
                            input_deck += f"    mesh_vector{i} = {vector}\n"
                        else:
                            input_deck += f"    # Error: mesh_vector{i} must have exactly 3 components\n"
                    except ValueError:
                        input_deck += f"    # Error: Invalid format for mesh_vector{i}\n"
        
        if domain.number_of_refinement_steps is not None or domain.number_of_refinement_steps != 0:
            input_deck += f"    number_of_refinement_steps = {domain.number_of_refinement_steps}\n"
        if domain.atomistic_domains:
            input_deck += f"    atomistic_domains = {domain.atomistic_domains}\n"
        
        # Boolean fields
        for bool_field in ['automatic_minimal_point_on_atom', 'sanity_check', 'parallel']:
            default = False
            if bool_field == 'sanity_check':
                default = True
                
            if getattr(domain, bool_field) != default:
                input_deck += f"    {bool_field} = true\n"
        
        # Parallel-specific parameters
        if domain.parallel:
            for param in ['xmin_p', 'xmax_p', 'ymin_p', 'ymax_p', 'zmin_p', 'zmax_p']:
                value = getattr(domain, param)
                if value is not None:
                    input_deck += f"    {param} = {value}\n"
        
        if domain.num_geom_cpus is not None:
            input_deck += f"    num_geom_cpus = {domain.num_geom_cpus}\n"
        
        input_deck += "  }\n\n"

    # Geometry and Regions
    input_deck += "  Geometry {\n"
    # Regular Regions
    for region in regions:
        input_deck += "  Region {\n"
        input_deck += f"    shape = {region.shape}\n"
        input_deck += f"    tag = {region.tag}\n"
        input_deck += f"    region_number = {region.region_number}\n"
        input_deck += f"    priority = {region.priority}\n"
        input_deck += f"    min = ({region.min_x}, {region.min_y}, {region.min_z})\n"
        input_deck += f"    max = ({region.max_x}, {region.max_y}, {region.max_z})\n"
        input_deck += "  }\n\n"
    
    # Boundary Regions
    for boundary_region in boundary_regions:
        input_deck += "  Boundary_region {\n"
        input_deck += f"    shape = {boundary_region.shape}\n"
        input_deck += f"    tag = {boundary_region.tag}\n"
        input_deck += f"    region_number = {boundary_region.region_number}\n"
        input_deck += f"    priority = {boundary_region.priority}\n"
        input_deck += f"    work_plane = {boundary_region.work_plane}\n"
        input_deck += f"    plane_tolerance = {boundary_region.plane_tolerance}\n"
        input_deck += f"    axis_cut = {boundary_region.axis_cut}\n"
        
        # Handle rectangles
        if boundary_region.rectangles:
            rectangles_str = ", ".join([str(tuple(rect)) for rect in boundary_region.rectangles])
            input_deck += f"    rectangles = [{rectangles_str}]\n"
        
        # Add the 'add' parameter (assuming it's always the region_number)
        input_deck += f"    add = ({boundary_region.region_number})\n"
        
        input_deck += "  }\n\n"
    input_deck += "  }\n"

    # Solvers
    input_deck += " Solvers {\n"

    # NonlinearPoissonFEM Solvers
    for solver in NonlinearPoissonFEM.objects.all():
        input_deck += "  solver {\n"
        input_deck += f"    name = {solver.name}\n"
        input_deck += f"    type = {solver.type}\n"
        input_deck += f"    domain = {solver.domain.name}\n"
        
        if solver.active_regions.exists():
            total_regions = solver.active_regions.all()+boundary_regions
            solver_regions = ", ".join([str(region.region_number) for region in total_regions])
            input_deck += f"    active_regions = ({solver_regions})\n"
        
        # Boolean fields
        boolean_fields = [
            'Dirichlet_nodes_output', 'Newton_step_only', 'disable_init', 'disable_output',
            'disable_reinit', 'disable_reset_set', 'disable_solve', 'disable_step',
            'average_over_cell', 'calculate_density_only', 'custom_convergence_test',
            'do_input_initial_nonlinearpoisson_potential', 'do_nonlinearpoisson_outputs_xyz_format',
            'do_output_nonlinearpoisson_potential', 'do_output_potential_each_iteration',
            'do_outputs_from_density_solver', 'full_Newton_step', 'import_initial_potential_from_solver',
            'import_on_FEM_grid', 'ksp_monitor', 'node_potential_output', 'one_dim_output_average',
            'output_at_each_iteration', 'output_jacobian', 'output_norms', 'output_residual',
            'output_yz_integrated_density', 'poisson_vtk_mesh', 'set_initial_field',
            'set_initial_potential', 'solve_on_single_replica', 'solve_with_zero_density_first',
            'stop_if_diverged', 'use_average_density_as_a_guess', 'use_classical_jacobian'
        ]
        
        for field in boolean_fields:
            if getattr(solver, field):
                input_deck += f"    {field} = true\n"
        
        # Numeric fields
        numeric_fields = [
            'CB_initial_shift', 'VB_initial_shift', 'abs_tolerance', 'chem_pot',
            'constant_initial_potential', 'equilibrium_el_chem_pot', 'field',
            'interpolation_power', 'linear_solver_maxit', 'max_function_evals',
            'max_iterations', 'max_nonlinear_step', 'number_of_interpolation_points',
            'number_of_output_points', 'potential_at_initial_point', 'rel_tolerance',
            'shift_copied_solution_by_voltage', 'step_abs_tolerance', 'step_rel_tolerance',
            'tolerance_in_terms_of_doping'
        ]
        
        for field in numeric_fields:
            value = getattr(solver, field)
            if value is not None:
                input_deck += f"    {field} = {value}\n"
        
        # Text fields
        text_fields = [
            'init', 'output', 'reinit', 'solve', 'step', 'atomistic_output',
            'boundary_condition', 'boundary_regions', 'charge_model', 'confined_band_solvers',
            'copy_solution_from', 'density_solver', 'dependent_solvers', 'external_object_name',
            'external_output', 'external_solver', 'fem_output', 'friends',
            'initial_potential_file_name', 'initial_potential_point', 'initial_potential_source',
            'ksp_type', 'linear_solver_family', 'one_dim_output', 'output_dependent_solvers',
            'output_file_suffix', 'output_line_corners', 'pc_type', 'petsc_solver_algorithm',
            'restart_data_input_file', 'restart_data_output_file', 'surface_of_regions', 'tic_toc_name'
        ]
        
        for field in text_fields:
            value = getattr(solver, field)
            if value:
                input_deck += f"    {field} = {value}\n"
        
        # Add boundary conditions for this solver
        solver_boundary_conditions = [bc for bc in boundary_conditions if bc.solver_model_name == solver.name]
        for bc in solver_boundary_conditions:
            input_deck += "    boundary_condition {\n"
            input_deck += f"      name = {bc.name}\n"
            input_deck += f"      type = {bc.type}\n"
            input_deck += f"      voltage = {bc.voltage}\n"
            input_deck += f"      surface_of_regions = ({bc.surface_of_regions})\n"
            input_deck += f"      single_surface_normal = ({bc.single_surface_normal})\n"
            input_deck += "    }\n"

        input_deck += "  }\n\n"

    # EMSchrodingerFEM Solvers
    for solver in EMSchrodingerFEM.objects.all():
        input_deck += "  solver {\n"
        input_deck += f"    name = {solver.name}\n"
        input_deck += f"    type = {solver.type}\n"
        input_deck += f"    domain = {solver.domain.name}\n"

        if solver.active_regions.exists():
            first_set = [str(region.region_number) for region in solver.active_regions.all()]
            second_set = [str(region.region_number) for region in boundary_regions]
            total_set = first_set + second_set
            em_regions = ", ".join(total_set)
            input_deck += f"    active_regions = ({em_regions})\n"
        print('DONE')
        # Fields with specific choices
        choice_fields = ['eigensolver', 'spectrum_position', 'pc_type', 'valley', 'longitudinal_effective_mass_direction', 'quadrature_rule']
        for field in choice_fields:
            value = getattr(solver, field)
            if value:
                input_deck += f"    {field} = {value}\n"
        
        # Numeric fields
        numeric_fields = [
            'number_of_eigenvalues', 'max_linear_solver_iterations', 'linear_solver_tolerance',
            'temperature', 'chemical_potential', 'B_field', 'g_factor', 'finite_element_order',
            'FEM_integration_order', 'max_refinement_iterations', 'max_refinement_level',
            'refine_fraction', 'coarsen_fraction', 'tolerance', 'valley_degeneracy',
            'valley_splitting', 'll_width_to_splitting_ratio', 'number_of_basis_vectors',
            'number_of_output_points'
        ]
        for field in numeric_fields:
            value = getattr(solver, field)
            if value is not None:
                input_deck += f"    {field} = {value}\n"
        
        # Boolean fields
        boolean_fields = [
            'use_density_interpolation', 'integrate_density', 'use_exchange_potential',
            'use_multiple_variables_for_spin_valley', 'print_energy_levels',
            'print_num_electrons_under_Ef', 'orthogonalize_interpolated_eigenvectors'
        ]
        for field in boolean_fields:
            if getattr(solver, field):
                input_deck += f"    {field} = true\n"
        
        # Text fields
        text_fields = [
            'potential_solver', 'finite_element_family', 'output_file_suffix', 'ksp_type',
            'linear_solver_family', 'predictor_type', 'density_integration_regions',
            'fem_output', 'eigen_vector_output_points_file', 'eigen_vectors_interpolated_points_shift',
            'approx_module', 'potential_type', 'tic_toc_name', 'd1_domain', 'd2_domain',
            'd1_eigensolver', 'output_line_corners'
        ]
        for field in text_fields:
            value = getattr(solver, field)
            if value:
                input_deck += f"    {field} = {value}\n"
        
        # Special handling for '_disable_output', '_search_flag', '_trigger_flag'
        if solver._disable_output:
            input_deck += f"    _disable_output = true\n"
        if solver._search_flag is not None:
            input_deck += f"    _search_flag = {solver._search_flag}\n"
        if solver._trigger_flag is not None:
            input_deck += f"    _trigger_flag = {solver._trigger_flag}\n"
            
        input_deck += "  }\n"

        input_deck += "  }\n\n"

    for solver in SemiclassicalFEM.objects.all():
        input_deck += "  solver {\n"
        input_deck += f"    name = {solver.name}\n"
        input_deck += f"    type = {solver.type}\n"
        input_deck += f"    domain = {solver.domain.name}\n"
        
        if solver.active_regions.exists():
            first_set = [str(region.region_number) for region in solver.active_regions.all()]
            second_set = [str(region.region_number) for region in boundary_regions]
            total_set = first_set + second_set
            joined_regions = ", ".join(total_set)
            input_deck += f"    active_regions = ({joined_regions})\n"


        # Numeric fields
        numeric_fields = [
            'dimension', 'electron_chem_pot', 'electron_temperature',
            'hole_chem_pot', 'hole_temperature'
        ]
        for field in numeric_fields:
            value = getattr(solver, field)
            if value is not None:
                input_deck += f"    {field} = {value}\n"
        
        # Text fields
        text_fields = [
            'output_file_suffix', 'param_type', 'tic_toc_name'
        ]
        for field in text_fields:
            value = getattr(solver, field)
            if value:
                input_deck += f"    {field} = {value}\n"
        
        # Special handling for '_disable_output', '_search_flag', '_trigger_flag'
        if solver._disable_output:
            input_deck += f"    _disable_output = true\n"
        if solver._search_flag is not None:
            input_deck += f"    _search_flag = {solver._search_flag}\n"
        if solver._trigger_flag is not None:
            input_deck += f"    _trigger_flag = {solver._trigger_flag}\n"
        
        input_deck += "  }\n\n"

    input_deck += "}\n\n"
    
    # Get the names of all solvers
    semiclassical_names = [solver.name for solver in semiclassical_solvers]
    poisson_names = [solver.name for solver in nonlinear_poisson_solvers]
    
    # Combine all solver names
    all_solver_names = semiclassical_names + poisson_names
    
    # Create the solve parameter string
    solve_string = ", ".join(all_solver_names)
    
    # Create the Global section
    input_deck += f"""Global {{
  solve = ({solve_string})
  database = ./all_GaAs_rev.mat
  messaging_level = 5
  temperature = 10
}}

"""

    return input_deck


def generate_input_deck_view(request):
    try:
        materials = Material.objects.all()
        domains = Domain.objects.all()
        regions = Region.objects.all()
        boundary_regions = BoundaryRegion.objects.all()
        nonlinear_poisson_solvers = NonlinearPoissonFEM.objects.all()
        em_schrodinger_solvers = EMSchrodingerFEM.objects.all()
        semiclassical_solvers = SemiclassicalFEM.objects.all()
        boundary_conditions = BoundaryCondition.objects.all()

        if not materials or not domains or not regions:
            return HttpResponse("Error: No data available to generate input deck.", status=400)
        input_deck_content = generate_input_deck(materials, domains, regions,nonlinear_poisson_solvers, em_schrodinger_solvers, semiclassical_solvers, boundary_conditions,boundary_regions)
        response = HttpResponse(input_deck_content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="input_deck.in"'
        return response
    except ObjectDoesNotExist:
        return HttpResponse("Error: Required data is missing.", status=400)
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)
