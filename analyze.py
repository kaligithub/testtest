########### Python Form Recognizer Async Analyze #############
import json
import time
import getopt
import sys
import os
from requests import get, post

class azureFormRecognizer:
    def __init__(self):
        pass

    @staticmethod
    def inferrType(input_file):
        filename, file_extension = os.path.splitext(input_file)
        if file_extension == '':
            print('File extension could not be inferred from inputfile. Provide type as an argument.')
            sys.exit()
        elif file_extension == '.pdf':
            return 'application/pdf'
        elif file_extension == '.jpeg':
            return 'image/jpeg'
        elif file_extension == '.bmp':
            return 'image/bmp'
        elif file_extension == '.png':
            return 'image/png'
        elif file_extension == '.tiff':
            return 'image/tiff'
        else:
            print('File extension ' + file_extension + ' not supported')
            sys.exit()

    @staticmethod
    def runAnalysis(input_file, file_type):
        # Endpoint URL
        dict = {}
        endpoint = r"https://sompoform.cognitiveservices.azure.com/"
        # Subscription Key
        apim_key = "b7c73850a0304265b036367afafdbf56"
        # Model ID
        model_id = "6c5b5d7f-5bd5-4ef4-9513-8428a0818933"
        # API version
        API_version = "v2.1"

        post_url = endpoint + "/formrecognizer/%s/custom/models/%s/analyze" % (API_version, model_id)
        params = {
            "includeTextDetails": True
        }

        headers = {
            # Request headers
            'Content-Type': file_type,
            'Ocp-Apim-Subscription-Key': apim_key,
        }
        try:
            with open(input_file, "rb") as f:
                data_bytes = f.read()
        except IOError:
            print("Inputfile not accessible.")
            sys.exit(2)

        try:
            print('Initiating analysis...')
            resp = post(url=post_url, data=data_bytes, headers=headers, params=params)
            if resp.status_code != 202:
                print("POST analyze failed:\n%s" % json.dumps(resp.json()))
                quit()
            print("POST analyze succeeded:\n%s" % resp.headers)
            get_url = resp.headers["operation-location"]
        except Exception as e:
            print("POST analyze failed:\n%s" % str(e))
            quit()

        n_tries = 5
        n_try = 0
        wait_sec = 20
        max_wait_sec = 100
        print()
        print('Getting analysis results...')
        while n_try < n_tries:
            try:
                resp = get(url=get_url, headers={"Ocp-Apim-Subscription-Key": apim_key})
                if resp.status_code != 200:
                    print("GET analyze results failed:\n%s" % json.dumps(resp_json))
                    quit()
                resp_json = resp.json()
                status = resp_json["status"]
                if status == "succeeded":
                    result = resp_json["analyzeResult"]["documentResults"]
                    #import pdb; pdb.set_trace()
                    for recognized_form in result:
                        # print("Form type: {}".format(recognized_form['docType']))
                        # print("Form type confidence: {}".format(recognized_form['docTypeConfidence']))
                        # print("Form was analyzed using model with ID: {}".format(recognized_form['model_id']))
                        for key in recognized_form['fields']:
                            try:
                                dict.update({key: recognized_form['fields'][key]['text']})
                                # print(key, recognized_form['fields'][key]['text'])
                            except:
                                dict.update({key: ""})
                                # print(key, "")
                    # if output_file:
                    #     with open(output_file, 'w') as outfile:
                    #         json.dump(dict, outfile, indent=2, sort_keys=True)
                    print(input_file)
                    print("Analysis succeeded:\n%s" % json.dumps(dict, indent=2, sort_keys=True))
                    quit()
                if status == "failed":
                    print("Analysis failed:\n%s" % json.dumps(resp_json))
                    quit()
                # Analysis still running. Wait and retry.
                time.sleep(wait_sec)
                n_try += 1
                wait_sec = min(2 * wait_sec, max_wait_sec)
            except Exception as e:
                msg = "GET analyze results failed:\n%s" % str(e)
                print(msg)
                quit()
        print("Analyze operation did not complete within the allocated time.")
        return dict

    # @staticmethod
    # def main():
    #     #input_file, output_file, file_type = getArguments(argv)
    #     file_base_name = os.path.basename(input_file)
    #     file_name, ext_name = os.path.splitext(file_base_name)
    #     file_type = ''
    #     if not file_type:
    #         file_type = azureFormRecognizer.inferrType(input_file)
    #     print(input_file, "\n", file_name, "\n", output_file, "\n", file_type)
    #     azureFormRecognizer.runAnalysis(input_file, output_file, file_type)

# if __name__ == '__main__':
#     #main(sys.argv[1:])
#     #input_file = r"C:\Users\sandeep.4.gupta.INCOFORGETECH\Documents\Sompo\sompo_training\ab2\Type 1\do-proposal-form.pdf"
#     azureFormRecognizer.main()

# def getArguments(argv):
#     input_file = ''
#     file_type = ''
#     output_file = ''
#     try:
#         opts, args = getopt.gnu_getopt(argv, "ht:o:", [])
#     except getopt.GetoptError:
#         printCommandDescription(2)
#
#     for opt, arg in opts:
#         if opt == '-h':
#             printCommandDescription()
#
#     if len(args) != 1:
#         printCommandDescription()
#     else:
#         input_file = args[0]
#
#     for opt, arg in opts:
#         if opt == '-t':
#             if arg not in ('application/pdf', 'image/jpeg', 'image/png', 'image/tiff', 'image/bmp'):
#                 print('Type ' + file_type + ' not supported')
#                 sys.exit()
#             else:
#                 file_type = arg
#
#         if opt == '-o':
#             output_file = arg
#             try:
#                 open(output_file, 'a')
#             except IOError:
#                 print("Output file not creatable")
#                 sys.exit(2)
#
#     if not file_type:
#         file_type = inferrType(input_file)
#
#     return (input_file, output_file, file_type)



# def printCommandDescription(exit_status=0):
#     print('analyze.py <inputfile> [-t <type>] [-o <outputfile>]')
#     print
#     print('If type option is not provided, type will be inferred from file extension.')
#     sys.exit(exit_status)

