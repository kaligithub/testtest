from analyze import azureFormRecognizer
import os

if __name__ == '__main__':
    #main(sys.argv[1:])
    # for path, subdirs, files in os.walk('./inputs'):
    #     for name in files:
    #         print(os.path.join(path, name))
    input_file = r"C:\Users\kalicharan.s\Downloads\Testing Sample\Type 1 - Done\21-05-10_Corporate_Guard_DO_Proposal_Form_completed and signed.pdf"
    file_base_name = os.path.basename(input_file)
    file_name, ext_name = os.path.splitext(file_base_name)
    output_file = r"D:\cfdev\test" + "\\" + file_name + ".json"
    # input_file, output_file, file_type = getArguments(argv)
    file_type = ''
    if not file_type:
        file_type = azureFormRecognizer.inferrType(input_file)
    #print(input_file, "\n", file_name, "\n", output_file, "\n", file_type)
    azureFormRecognizer.runAnalysis(input_file, file_type)
