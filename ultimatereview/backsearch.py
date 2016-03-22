def main(query,sort,number):

        import urllib
        import sys
        import webbrowser

        def convertQuery(query):        #replaces spaces in a string with "+"'s so the string will be suitable for use in a url
                output = ""
                for i in query:
                        if i == " ":
                                output += "+"
                        else:
                                output += i
                return output

        def searchURL(query,sort,number):           #takes a query, sort type, and number of articles to create a url leading to a list of ID's
                nurl = "esearch.fcgi?db=PubMed&retmax=" + number + "&sort=" + sort + "&term=" + query
                return nurl

        def fetchURL(id):                           #takes a pubmed document ID and creates the url that leads to the document
                nurl = "efetch.fcgi?db=PubMed&id="
                nurl += str(id)
                nurl += "&rettype=fasta&retmode=text"
                return nurl

        def summaryURL(id):
                nurl = "esummary.fcgi?db=PubMed&id="
                nurl += str(id)
                return nurl

        def removeBrackets(inp):        #removes anything between and including < > brackets
                out = ""                    #allows processing of the html
                add = 1
                for c in inp:
                        if c == "<":
                                add = 0
                        elif c == ">":
                                add = 1
                        elif add == 1:
                                out += c
                return out

        def fetchExtract(source,info):
                start = "<" + info + ">"
                end = "</" + info + ">"
                startPos = source.find(start) + len(start)
                endPos = source.find(end) - 1
                return source[startPos:endPos]

        def summaryExtract(source,info):
                authorList = []
                index = 0
                while source.find(info,index)>0:
                        output = ""
                        add = 0
                        index = source.find(info,index)
                        while source[index] != "<":
                                if add == 1:
                                        output += source[index]
                                        index+=1
                                elif source[index] == ">":
                                        add = 1
                                        index+=1
                                else:
                                        index+=1
                        authorList += [output]
                                if len(authorList)>0:
                                        if info == "Author":
                                                return authorList[1:-1]
                                        else:
                                                return authorList[0]
                                else:
                                        return authorList


        query = convertQuery(query)

        url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/"       #base url that all PubMed interaction goes through
        page = urllib.urlopen(url + searchURL(convertQuery(query),sort,number))     #opens page for given query and sets it to 'page' variable
        source = page.read()
        idList = removeBrackets(fetchExtract(source,"IdList")).split() #Removes brackets for the string containing the ID list, and splits into a list of each ID
        docList = []

        for u in idList:                #generates a new list containing each ID's respective url
                document = {}
                currentURL = fetchURL(u)
                p = urllib.urlopen(url + currentURL)
                source = p.read()
                document = {'url': url + currentURL, 'abstract': source, 'id':u}
                p.close
                p = urllib.urlopen(url + summaryURL(u))
                source = p.read()
                document['author'] = summaryExtract(source,"Author")
                document['title'] = summaryExtract(source,"Title")
                docList += [document]
        return docList
