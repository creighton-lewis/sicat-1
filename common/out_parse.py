from colorama import Fore, Back, Style
import re
import os
import json
import pyaml
class Output:
    def __init__(self):
        self.data = []
    
    def banner(self):
        ascii_art = f"""
_._     _,-'""`-._
(,-.`._,'(       |\`-/|
    `-.-' \ )-`( , {Fore.RED}o o{Fore.WHITE})
        `-    \`_`"'-
{Fore.RED}SiCat{Fore.WHITE} - The useful {Fore.RED}exploit{Fore.WHITE} finder
@justakazh (https://github.com/justakazh/sicat)

usage : sicat.py --help
        """
        print(ascii_art)

    def start(self,keyword = "", version = ""):
        print("|")
        print(f"|{Fore.YELLOW}> Starting with Keyword : {keyword} {version} {Fore.WHITE}")
        print("|----------------------------------------")

    def exploitdb(self, content):
        try:
            if len(content['data']) != 0:
                print("|")
                print(f"|{Fore.GREEN}+ Exploit-DB Result {Fore.WHITE}")
                print("|--------------------")

                predata = []
                for data in content['data']:
                    print(f"|{Fore.BLUE}-{Fore.WHITE} Title : {data['description'][1]}")
                    print(f"|{Fore.BLUE}-{Fore.WHITE} Type  : {data['type_id']}")
                    print(f"|{Fore.BLUE}-{Fore.WHITE} Link  : https://www.exploit-db.com/exploits/{data['description'][0]}")
                    print("|")
                    print("|")

                    predata.append({
                        "title" : data['description'][1],
                        "type" : data['type_id'],
                        "link" : f"https://www.exploit-db.com/exploits/{data['description'][0]}"
                    })
                print(f"|{Fore.BLUE}-{Fore.WHITE} Total Result : {Fore.GREEN}{len(content['data'])}{Fore.WHITE} Exploits Found!")
                self.data.append({"exploitdb" : predata})
            else:
                print(f"|{Fore.RED}- No result in ExploitDB!{Fore.WHITE}")
        except:
            print(f"|{Fore.RED}- Internal Error - No result in ExploitDB!{Fore.WHITE}")


    def msfmodule(self, content):
        try:
            if len(content) != 0:
                print("|")
                print(f"|{Fore.GREEN}+ Metasploit Module Result {Fore.WHITE}")
                print("|------------------------------")


                predata = []
                for data in content:
                    print(f"=================================================================")
                    print(f"|{Fore.BLUE}-{Fore.WHITE} Title : {data['title'].capitalize()}")
                    print(f"|{Fore.BLUE}-{Fore.WHITE} Module : {data['module']}")
                    print(f"|{Fore.BLUE}-{Fore.WHITE} Link : {data['link']}")
                   # print(f"|{Fore.BLUE}-{Fore.WHITE} References : {data['references']}")

                    if 'references' in data and data['references']:
                        references = data['references']
                    if isinstance(references, list):
                        print(f"|{Fore.BLUE}-{Fore.WHITE} References:{Style.RESET_ALL}")
                    for i, ref in enumerate(references):
                        print(f"|    {Fore.CYAN}{i+1}. {ref}{Style.RESET_ALL}") # Indented and numbered
                    else:
        # If it's not a list (e.g., a single string), print it directly
                    #    print(f"|{Fore.BLUE}-{Fore.WHITE} References : {references}{Style.RESET_ALL}")

                   # print("|")
                  #  print("|")

                        predata.append({
                        "title" : data['title'],
                        "module" : data['module'],
                        "link" : data['link'],
                        "references" : data['references']
                    })
                print(f"|{Fore.BLUE}-{Fore.WHITE} Total Result : {Fore.GREEN}{len(content)}{Fore.WHITE} Modules Found!")
                self.data.append({"msfmodule" : predata})
            else:
                print(f"|{Fore.RED}- No result in Metasploit Module!{Fore.WHITE}")
        except:
            print(f"|{Fore.RED}- Internal Error - No result in Metasploit Module!{Fore.WHITE} ")


    def nvddb(self, content):
        try:
            if len(content['vulnerabilities']) != 0:
                print("|")
                print(f"|{Fore.GREEN}+ National Vulnearbility Database Result {Fore.WHITE}")
                print("|-----------------------------------------------")

                predata = []
                for data in content['vulnerabilities']:
                    print(f"|{Fore.BLUE}-{Fore.WHITE} ID : {data['cve']['id']}")
                    print(f"|{Fore.BLUE}-{Fore.WHITE} Description : {data['cve']['descriptions'][0]['value']}")
                    print(f"|{Fore.BLUE}-{Fore.WHITE} Link : https://nvd.nist.gov/vuln/detail/{data['cve']['id']}")
                    print("|")
                    print("|")

                    predata.append({
                        "title" : data['cve']['id'],
                        "description" : data['cve']['descriptions'][0]['value'],
                        "link" : f"https://nvd.nist.gov/vuln/detail/{data['cve']['id']}"
                    })
                print(f"|{Fore.BLUE}-{Fore.WHITE} Total Result : {Fore.GREEN}{len(content)}{Fore.WHITE} CVEs Found!")
                self.data.append({"nvddb" : predata})
            else:
                print("|")
                print(f"|{Fore.RED}- No result in National Vulnearbility Database!{Fore.WHITE}")
        except:
            print(f"|{Fore.RED}- Internal Error - No result in National Vulnearbility Database!{Fore.WHITE}")
            

    def outJson(self, location = ""):
        self.genOutDir(location)
        report = json.dumps(self.data, indent=4)
        open(f"{location}/report.json", "w").write(report)

    def outYaml(self, file, location=""):
        """Export data to YAML."""
        import yaml
        yaml = pyaml
        self.genOutDir(location)
        report = yaml.dump(self.data, indent=4, sort_keys=False)
        with open (f"{file}report.yaml", "w", encoding="utf-8") as f:
        #with open(f"{location}/report.yaml", "w", encoding="utf-8") as f:
            f.write(report)  

    def outHtml(self, location = ""):
        self.genOutDir(location)
        html = """
<!DOCTYPE html> <html lang="en"> <head> <meta charset="UTF-8"> <meta name="viewport" content="width=device-width, initial-scale=1.0"> <title>SiCat Report</title> <link rel="stylesheet" href="https://cdn.datatables.net/1.13.7/css/jquery.dataTables.css" /> <style> body{ font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif; margin: 0 20%; font-size: 14px; } header{ background-color: #205499; padding: 4px; color:white; text-align: center; } footer{ margin-top: 50px !important; background-color: #205499; padding: 4px; padding-bottom: 20px; color:white; text-align: center; } .row{ padding: 0 3%; margin-top: 5%; } header a, footer a{ color:white } a{ text-decoration: none; } a:hover{ text-decoration: underline; } .visit{ color:white; background-color: #205499; padding: 4px; border-radius: 4px; } .visit:hover{ color:white; background-color: #173f72; text-decoration: none; } </style> </head> <body> <header> <h1>SiCat Report</h1> <p > The useful exploit finder </p> <p> <a href="">https://github.com/justakazh/sicat</a> </p> </header> <!-- Sumary --> <div class="row"> <h2>Summary</h2> <p> SiCat is an advanced exploit search tool designed to identify and gather information about exploits from both open sources and local repositories effectively. With a focus on cybersecurity, SiCat allows users to quickly search online, finding potential vulnerabilities and relevant exploits for ongoing projects or systems. </p> <p> SiCat's main strength lies in its ability to traverse both online and local resources to collect information about relevant exploitations. This tool aids cybersecurity professionals and researchers in understanding potential security risks, providing valuable insights to enhance system security. </p> </div>"""

        for report in self.data:
            if "exploitdb" in report:
                html += """<div class="row"><h2>Exploit-DB</h2><table id="exploitdb" class="display"><thead><tr><th>#</th><th>Title</th><th>Type</th><th>Link</th></tr></thead><tbody>"""
                num = 1
                for exploitdb in report['exploitdb']:
                    html += f"<tr><td>{num}</td><td>{exploitdb['title']}</td><td>{exploitdb['type']}</td><td><a target='_blank' href='{exploitdb['link']}'class='visit'>visit</a></td></tr>"
                    num += 1
                html += """</tbody></table></div>"""
            
            if "exploitalert" in report:
                html += """<div class="row"> <h2>ExploitAlert</h2> <table id="exploitalert" class="display"> <thead> <tr> <th>#</th> <th>Title</th> <th>Link</th> </tr> </thead> <tbody>"""
                num = 1
                for exploitalert in report['exploitalert']:
                    html += f"<tr><td>{num}</td><td>{exploitalert['title']}</td><td><a target='_blank' href='{exploitalert['link']}'class='visit'>visit</a></td></tr>"
                    num += 1
                html += """</tbody></table></div>"""
        

            if "nvddb" in report:
                html += """<div class="row"> <h2>NVD Database</h2> <table id="nvddb" class="display"> <thead> <tr> <th style="width: 14%;">ID</th> <th>Description</th> <th>Link</th> </tr> </thead> <tbody>"""
                for nvd in report['nvddb']:
                    html += f"<tr><td>{nvd['title']}</td><td>{nvd['description']}</td><td><a target='_blank' href='{nvd['link']}'class='visit'>visit</a></td></tr>"
                html += """</tbody></table></div>"""
            
            if "msfmodule" in report:
                html += """<div class="row"> <h2>Metasploit Module</h2> <table id="msfmodule" class="display"> <thead> <tr> <th>#</th> <th>Titke</th> <th>Module</th> <th>Link</th> </tr> </thead> <tbody>"""
                num = 1
                for msf in report['msfmodule']:
                    html += f"<tr> <td>{num}</td> <td>{msf['title']}</td> <td>{msf['module']}</td> <td> <a target='_blank' href='{msf['link']}' class='visit'>Visit</a> </td> </tr>"
                    num += 1
                html += """</tbody></table></div>"""


        html += """<footer><h4>Thank You for using SiCat!</h4><ul style="list-style: none;"><li style="margin-top:10px;">Give us star: <a href="">https://github.com/justakazh/sicat</a></li></ul></footer><script src="https://code.jquery.com/jquery-3.7.1.min.js"></script><script src="https://cdn.datatables.net/1.13.7/js/jquery.dataTables.js"></script><script>$(document).ready( function () {$('#exploitdb').DataTable();$('#exploitalert').DataTable();$('#packetstorm').DataTable();$('#nvddb').DataTable();$('#msfmodule').DataTable();} );</script></body></html>"""

        open(f"{location}/report.html", "w").write(html)
    

    def genOutDir(self,locate):
        try:
            os.makedirs(locate, exist_ok=True)
        except:
            pass

