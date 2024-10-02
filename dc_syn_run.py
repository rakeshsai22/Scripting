import os
import subprocess
import itertools

base_template_path = '/home/snakkill/Autosynth/journal/dc_syn/tcl/base.tcl'

def create_tcl_script(design_name, design_files, clock_period, clock_name, run_id, work_lib_dir, output_directory, optimization_command_1, compile_command_1, optimization_command_2, compile_command_2):
    with open(base_template_path, 'r') as file:
        base_tcl_script = file.read()

    verilog_files = "\n".join([f'read_verilog "{file}"' for file in design_files])

    tcl_script_path = os.path.join(output_directory, f'run_{run_id}.tcl')

    with open(tcl_script_path, 'w') as file:
        file.write(base_tcl_script.format(
            design_name=design_name,
            verilog_files=verilog_files,
            clock_period=clock_period,
            clock_name=clock_name,
            output_directory=output_directory,
            run_id=run_id,
            work_lib_dir=work_lib_dir,
            optimization_command_1=optimization_command_1,
            compile_command_1=compile_command_1,
            optimization_command_2=optimization_command_2,
            compile_command_2=compile_command_2
        ))

    return tcl_script_path

def find_verilog_files(directory):
    verilog_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.v'):
                verilog_files.append(os.path.join(root, file))
    return verilog_files

def run_synthesis(run_id, tcl_script_path, output_directory):
    log_file_path = os.path.join(output_directory, f'run_{run_id}_log.txt')
    error_file_path = os.path.join(output_directory, f'run_{run_id}_error.txt')
    print(f"Launching synthesis run {run_id} for {tcl_script_path}...\n")
    
    with open(log_file_path, 'w') as log_file, open(error_file_path, 'w') as error_file:
        process = subprocess.Popen(['dc_shell', '-f', tcl_script_path], stdout=log_file, stderr=error_file)
    return process

def main():
    results_folder = '/home/snakkill/Autosynth/journal/results/exploration'
    clock_period = 2

    if not os.path.exists(results_folder):
        os.makedirs(results_folder, exist_ok=True)

    design_directories = {
        "wb_conmax_top": ("/home/snakkill/Autosynth/journal/dc_syn/verilog/Archive-2/wb_conmax", "clk_i"),
        "mips_16_core_top": ("/home/snakkill/Autosynth/journal/dc_syn/verilog/mips_16-master/rtl", "clk"),
        "usbf_top": ("/home/snakkill/Autosynth/journal/dc_syn/verilog/Archive-2/usb_funct", "clk_i"),
        "aes": ("/home/snakkill/Autosynth/journal/dc_syn/verilog/Archive-2/systemcaes", "clk"),
        "pci_bridge32": ("/home/snakkill/Autosynth/journal/dc_syn/verilog/Archive-2/pci", "wb_clock_in"),
        "wb_dma_top": ("/home/snakkill/Autosynth/journal/dc_syn/verilog/Archive-2/wb_dma", "clk_i"),
        "des": ("/home/snakkill/Autosynth/journal/dc_syn/verilog/Archive-2/systemcdes", "clk")
    }

    optimization_command_1_list = ["# No optimization commands"]
    optimization_command_2_list = ["# No optimization commands"]
    compile_command_1_list = ["compile"]
    compile_command_2_list = ["# No second compile command"]

    command_combinations = list(itertools.product(optimization_command_1_list, compile_command_1_list, optimization_command_2_list, compile_command_2_list))

    run_id = 1
    processes = []

    for design_name, (directory, clock_name) in design_directories.items():
        verilog_files = find_verilog_files(directory)

        for optimization_command_1, compile_command_1, optimization_command_2, compile_command_2 in command_combinations:
            # Print possible run configuration
            print(f"Run {run_id}: {design_name} | {optimization_command_1}, {compile_command_1}, {optimization_command_2}, {compile_command_2}")

            output_directory = os.path.join(results_folder, f'run_{run_id}')
            work_lib_dir = os.path.join(output_directory, "work_lib")

            os.makedirs(output_directory, exist_ok=True)
            os.makedirs(work_lib_dir, exist_ok=True)

            tcl_script_path = create_tcl_script(
                design_name,
                verilog_files,
                clock_period,
                clock_name,
                run_id,
                work_lib_dir,
                output_directory,
                optimization_command_1,
                compile_command_1,
                optimization_command_2,
                compile_command_2
            )

            # Launch the synthesis process
            process = run_synthesis(run_id, tcl_script_path, output_directory)
            processes.append(process)
            run_id += 1

    # Wait for processes to finish
    for p in processes:
        p.wait()
        print(f"Synthesis run {run_id} completed.")

    print("All synthesis runs completed successfully.")

if __name__ == "__main__":
    main()
