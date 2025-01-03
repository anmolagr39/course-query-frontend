from groq import Groq
import os
import chromadb
import asyncio
from pymongo import MongoClient

MONGO_URI = "mongodb+srv://sakshamrohatgi10:Saksham123@cluster0.3pfxs.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"  # Replace with your MongoDB URI
DATABASE_NAME = "text_files_db"
COLLECTION_NAME = "files"

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]
# Initialize Chroma HTTP Client
# client_chroma = chromadb.HttpClient()
# collection_name = "Handbot2"
# try:
#     collection = client_chroma.get_collection(collection_name)
# except ValueError:
#     print(f"Collection '{collection_name}' not found. Please create it first.")
#     exit()


def get_llama_response(user_prompt):
    client = Groq(
        api_key="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")  # Replace with your actual API key

    fixed_prefix = """
            This is a two-step process:
            1. Extract EXACT keywords from the input question that could be a course identifier. The keywords must appear in the question exactly as you extract them - do not modify, reword or interpret them. Examples:
            - Question: "Who teaches CHEM F111?" → Extract: CHEM F111
            - Question: "What's in Machine Learning?" → Extract: Machine Learning
            - Question: "When does Neural Networks start?" → Extract: Neural Networks

            If no clear course identifier exists, output "None". Also use common sense and give relevant outputs. Not neccessary that you will always get a clear case to match.

            2. **For course matching:** ONLY if step 1 found keywords: Compare the EXACT extracted keywords against this course list. Use fuzzy matching to account for minor typos or variations. Return the item in the list with the highest similarity score where the extracted keywords most closely align with a course name in the list else Return "None" if there is not a strong match.



            [course list follows]
        BIOT_F424_FOOD_BIOTECHNOLOGY.txt
        BIO_F110_BIOLOGY_LABORATORY.txt
        BIO_F111_GENERAL_BIOLOGY.txt
        BIO_F211_BIOLOGICAL_CHEMISTRY.txt
        BIO_F212_MICROBIOLOGY.txt
        BIO_F213_CELL_BIOLOGY.txt
        BIO_F214_INTEGRATED_BIOLOGY.txt
        BIO_F266_STUDY_PROJECT.txt
        BIO_F311_RECOMBINANT_DNA_TECH.txt
        BIO_F312_PLANT_PHYSIOLOGY.txt
        BIO_F313_ANIMAL_PHYSIOLOGY.txt
        BIO_F366_LABORATORY_PROJECT.txt
        BIO_F367_LABORATORY_PROJECT.txt
        BIO_F376_DESIGN_PROJECT.txt
        BIO_F377_DESIGN_PROJECT.txt
        BIO_F411_LABORATORY.txt
        BIO_F418_GENETIC_ENGINEERING_TECH.txt
        BIO_F421_ENZYMOLOGY.txt
        BIO_F491_SPECIAL_PROJECT.txt
        BIO_G523_ADV_&_APPLIED_MICROBIO.txt
        BIO_G524_ANIMAL_CELL_TECHNOLOGY.txt
        BIO_G525_ENV_BIOTECH_&_WASTE_MGMT.txt
        BIO_G526_CANCER_BIOLOGY.txt
        BIO_G532_BIOSTATISTICS_&_BIOMODEL.txt
        BIO_G542_ADVANCED_CELL_MOLE_BIO.txt
        BIO_G612_HUMAN_GENETICS.txt
        BITS_C790T_INDEPENDENT_STUDY.txt
        BITS_C791T_TEACHING_PRACTICE_I.txt
        BITS_C797T_PH_D_SEMINAR.txt
        BITS_C799T_PH_D_THESIS.txt
        BITS_E574_STUDY_IN_ADVANCED_TOPIC_II.txt
        BITS_E584_CASE_STUDIES_II.txt
        BITS_E594_READING_COURSE_II.txt
        BITS_E793T_PRACTICE_LECT_SERIES_I.txt
        BITS_F110_ENGINEERING_GRAPHICS.txt
        BITS_F111_THERMODYNAMICS.txt
        BITS_F112_TECHNICAL_REPORT_WRITING.txt
        BITS_F113_GENERAL_MATHEMATICS_I.txt
        BITS_F218_GENERAL_MATHEMATICS_III.txt
        BITS_F219_PROCESS_ENGINEERING.txt
        BITS_F225_ENVIRONMENTAL_STUDIES.txt
        BITS_F234_INTRO_TO_ENGG_DESIGN.txt
        BITS_F312_NEURAL_NET_&_FUZZY_LOGIC.txt
        BITS_F314_GAME_THEO_AND_ITS_APPL.txt
        BITS_F326_DESIGN_THINKING_FOR_INNOVATION.txt
        BITS_F343_FUZZY_LOGIC_&_APPL.txt
        BITS_F382_READING_COURSE.txt
        BITS_F385_INTRO_TO_GENDER_STUDIES.txt
        BITS_F386_QUANTUM_INFO_&_COMPUTING.txt
        BITS_F415_INTRODUCTION_TO_MEMS.txt
        BITS_F421T_THESIS.txt
        BITS_F422T_THESIS.txt
        BITS_F423T_THESIS.txt
        BITS_F424T_THESIS.txt
        BITS_F428_ESSENTIALS_OF_STRATE_MGT.txt
        BITS_F431_FLEXIBLE_MANUFAC_SYST.txt
        BITS_F446_PATTERN_RECOGNITION.txt
        BITS_F451_AUTONOMOUS_MOBILE_ROBOTICS.txt
        BITS_F452_BLOCKCHAIN_TECHNOLOGY.txt
        BITS_F462_RENEWABLE_ENERGY.txt
        BITS_F464_MACHINE_LEARNING.txt
        BITS_F467_BIOETHICS_&_BIOSAFETY.txt
        BITS_F468_NEW_VENTURE_CREATION.txt
        BITS_F469_FINANCING_INFRA_PROJECTS.txt
        BITS_F482_CREAT_&_LEAD_ENTREP_ORGN.txt
        BITS_F494_ENV_IMPACT_ASSESSMENT.txt
        BITS_G511_ADVANCED_PROJECT.txt
        BITS_G513_STUDY_IN_ADVANCED_TOPICS.txt
        BITS_G529_RESEARCH_PROJECT_I.txt
        BITS_G539_RESEARCH_PROJECT_II.txt
        BITS_G540_RESEARCH_PRACTICE.txt
        BITS_G553_REAL_TIME_SYSTEMS.txt
        BITS_G561T_DISSERTATION.txt
        BITS_G562T_DISSERTATION.txt
        BITS_G563T_DISSERTATION.txt
        BITS_G629T_DISSERTATION.txt
        BITS_G649_READING_COURSE.txt
        BITS_G661_RESEARCH_METHODOLOGY_I.txt
        BITS_N301T_PERSONAL_INT_LEAD_ORIENT_&_TW.txt
        CE_F211_MECHANICS_OF_SOLIDS.txt
        CE_F213_SURVEYING.txt
        CE_F230_CIVIL_ENGINEERING_MATERIALS.txt
        CE_F231_FLUID_MECHANICS.txt
        CE_F312_HYDRAULIC_ENGINEERING.txt
        CE_F313_FOUNDATION_ENGINEERING.txt
        CE_F320_DESIGN_OF_RE_CONCRETE_STRU.txt
        CE_F377_DESIGN_PROJECT.txt
        CE_F417_APP_OF_AI_IN_CIVIL_ENGG.txt
        CE_F419_GEOTECH_EQ_ENG_&_MC_FOUN.txt
        CE_F434_ENV_IMPACT_ASSESSMENT.txt
        CE_G515_FUNDAMENTALS_OF_SYS_ENGG.txt
        CE_G523_TRAN_SYST_PLAN_&_MANAGE.txt
        CE_G525_WATER_RESOUR_PLAN_&_MANA.txt
        CE_G527_CONSTRUCTION_MANAGEMENT.txt
        CE_G534_PAVEMENT_MATERIAL_CHARAC.txt
        CE_G547_PAV_FAIL_EVAL_&_REHABIL.txt
        CE_G549_RURAL_ROAD_TECHNOLOGY.txt
        CE_G551_DYNAMICS_OF_STRUCTURES.txt
        CE_G552_ADV_STR_MECH_&_STABILITY.txt
        CE_G565_TRANSPORTATION_PLANNING.txt
        CE_G567_HIGHWAY_DESIGN.txt
        CE_G568_TRAFFIC_SYSTEMS_ANALYSIS.txt
        CE_G612_ADVANCED_STEEL_STRUCTURE.txt
        CE_G614_PRESTRESS_CONCRETE_STRUC.txt
        CE_G616_BRIDGE_ENGINEERING.txt
        CE_G617_ADVANCE_STRUC_ANALYSIS.txt
        CE_G619_FINITE_ELEMENT_ANALYSIS.txt
        CE_G623_GROUND_IMPROVEMENT_TECH.txt
        CE_G632_DES_OF_FOUN_FOR_DYN_LOAD.txt
        CHEM_F110_CHEMISTRY_LABORATORY.txt
        CHEM_F111_GENERAL_CHEMISTRY.txt
        CHEM_F211_PHYSICAL_CHEMISTRY_I.txt
        CHEM_F212_ORGANIC_CHEMISTRY_I.txt
        CHEM_F213_PHYSICAL_CHEMISTRY_II.txt
        CHEM_F214_INORGANIC_CHEMISTRY_I.txt
        CHEM_F311_ORGANIC_CHEMISTRY_III.txt
        CHEM_F312_PHYSICAL_CHEMISTRY_IV.txt
        CHEM_F313_INSTRU_METHODS_OF_ANAL.txt
        CHEM_F323_BIOPHYSICAL_CHEMISTRY.txt
        CHEM_F327_ELECTROCHEM_FUNDA_&_APPL.txt
        CHEM_F330_PHOTOPHYSICAL_CHEMISTRY.txt
        CHEM_F333_CHEMISTRY_OF_MATERIALS.txt
        CHEM_F335_ORGANIC_CHEM_&_DRUG_DES.txt
        CHEM_F337_GREEN_CHEM_&_CATALYSIS.txt
        CHEM_F422_STATISTICAL_THERMODYNAM.txt
        CHEM_G521_ENVIRONMENTAL_CHEMISTRY.txt
        CHEM_G551_ADV_ORGANIC_CHEMISTRY.txt
        CHEM_G553_ADV_PHYSICAL_CHEMISTRY.txt
        CHE_F211_CHEMICAL_PROCESS_CALCULA.txt
        CHE_F212_FLUID_MECHANICS.txt
        CHE_F213_CHEM_ENGG_THERMODYNAMICS.txt
        CHE_F214_ENGINEERING_CHEMISTRY.txt
        CHE_F311_KINETICS_&_REACTOR_DESIG.txt
        CHE_F312_CHEMICAL_ENGG_LAB_I.txt
        CHE_F313_SEPARATION_PROCESSES_II.txt
        CHE_F314_PROCESS_DES_PRINCIPLES_I.txt
        CHE_F315_MACHINE_LEARNING_FOR_CHE_ENG.txt
        CHE_F411_ENVIR_POLLUTION_CONTROL.txt
        CHE_F422_PETROLEUM_REFINING_TECHNOLOGY.txt
        CHE_F425_ENVIRONMENTAL_MANAGEMENT_SYST.txt
        CHE_F497_ATOMIC_&_MOLECULAR_SIMULATION.txt
        CHE_G513_ENVIR_MANAGEMENT_SYSTEMS.txt
        CHE_G523_MATH_METHODS_IN_CHEM_ENG.txt
        CHE_G552_ADV_TRANSPORT_PHENOMENA.txt
        CHE_G553_STATISTIC_THERMODYNAMICS.txt
        CHE_G558_CHEM_PROC_OPTIMIZATION.txt
        CHE_G617_PETRO_REFINERY_ENGG.txt
        CS_F111_COMPUTER_PROGRAMMING.txt
        CS_F213_OBJECT_ORIENTED_PROG.txt
        CS_F214_LOGIC_IN_COMPUTER_SC.txt
        CS_F215_DIGITAL_DESIGN.txt
        CS_F222_DISCR_STRUC_FOR_COMP_SCI.txt
        CS_F301_PRINCIPLES_OF_PROGG_LANG.txt
        CS_F316_QUANTUM_ARCHITECTURE_AND_PROGR.txt
        CS_F320_FOUNDATIONS_OF_DATA_SCIENCE.txt
        CS_F342_COMPUTER_ARCHITECTURE.txt
        CS_F351_THEORY_OF_COMPUTATION.txt
        CS_F372_OPERATING_SYSTEMS.txt
        CS_F407_ARTIFICIAL_INTELLIGENCE.txt
        CS_F415_DATA_MINING.txt
        CS_F425_DEEP_LEARNING.txt
        CS_F426_GRAPH_MINING.txt
        CS_F429_NATURAL_LANGUAGE_PROCESSING.txt
        CS_F441_SEL_TOPICS_FROM_COMP_SC.txt

            Return your response in this exact format:
            Extracted: [extracted course identifier] (if applicable)
            Match: [exact matching filename from list or None if no match] (if course matching)



            **Examples:**
            Question: "Who teaches CHEM F111?"
            Extracted: CHEM F111
            Match: CHEM_F111_GENERAL_CHEMISTRY.txt

            Question: "What's for lunch?"
            Extracted: None
            Match: None

            Question: "Who teaches maths laboratory?"
            Extracted: maths laboratory
            Match: None

            Question: "what is the midsem exam date?"
            Extracted: None
            Match: None

            Question: "who is the instructor for deep learning?"
            Extracted: deep learning
            Match: CS_F425_DEEP_LEARNING.txt

            Question: "who is the instructor?"
            Extracted: None
            Match: None


            Question: "When does Deep Learning start and Machine Learning?"
            Extracted1: Deep Learning
            Extracted2: Machine Learning
            Match1: CS_F425_DEEP_LEARNING.txt
            Match2: BITS_F464_MACHINE_LEARNING.txt

            These are just few examples. use common sense to and examples intuition to decide whether there is a course mentioned or not.

            Take care of minor spelling mistakes and capitalization. If you find any error no need to state that. Rather just give me the final output in the desired form above.
            
            If you extract words like coding or something like an activity then Extracted: None Match: None.
            
            """

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": fixed_prefix
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True
    )
    temp_filename = "llama_response.txt"
    with open(temp_filename, "w") as file:
        for chunk in completion:
            file.write(chunk.choices[0].delta.content or "")
    with open(temp_filename, "r") as file:
        response = file.read()
    os.remove(temp_filename)
    return response


def parse_response(response):
    extracted = []
    matches = []
    lines = response.strip().split("\n")

    for line in lines:
        if line.startswith("Extracted"):
            extracted_values = line.split(":")[1].strip().split(",")  # Support multiple comma-separated extractions
            for extracted_val in extracted_values:
                if extracted_val.strip() and extracted_val.strip() != "None":
                    extracted.append(extracted_val.strip())
        elif line.startswith("Match"):
            match_values = line.split(":")[1].strip().split(",")  # Support multiple comma-separated matches
            for match_val in match_values:
                if match_val.strip() and match_val.strip() != "None":
                    matches.append(match_val.strip())
    return extracted, matches


async def perform_similarity_search(collection, query):
    try:
        result = collection.find_one({"filename": query})
        if result:
            return [result["filename"]], [result["content"]]
        else:
            return [], []
    except Exception as e:
        print(f"Error during similarity search: {e}")
        return [], []
    # except Exception as e:
    #     print(f"Error retrieving file from MongoDB: {e}")
    #     if results and "documents" in results and results["documents"] and results["documents"][0]:
    #         return results["documents"][0], results["metadatas"][0], results["distances"][0]
    #     else:
    #         return None, None, None
    # except Exception as e:
    #     print(f"Error during similarity search: {e}")
    #     return None, None, None

#
# def retrieve_file_by_filename(filename):
#     try:
#         # Find the document based on the filename
#         document = collection.find_one({"filename": filename})
#



async def perform_refined_llama_call(metadata_list, user_prompt):
    client = Groq(
        api_key="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")  # Replace with your actual API key

    refined_prompt = """
        Based on the following metadata of courses, refine your response to the user's query. Use the provided descriptions to compare courses as per the query. If metadata is not directly relevant, leverage it to enhance your response quality.

        Metadata:
        """
    for metadata in metadata_list:
        refined_prompt += f"- {metadata}\n"

    refined_prompt += f"\nUser's query: {user_prompt}\n"

    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "system",
                "content": refined_prompt
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True
    )
    temp_filename = "refined_llama_response.txt"
    with open(temp_filename, "w") as file:
        for chunk in completion:
            file.write(chunk.choices[0].delta.content or "")
    with open(temp_filename, "r") as file:
        response = file.read()
    os.remove(temp_filename)
    return response


async def process_query(user_prompt, previous_matches=None):
    llama_response = get_llama_response(user_prompt)
    extracted, matches = parse_response(llama_response)
    all_results = []
    metadata_list = []
    search_tasks = []
    refined_response = None

    if extracted and "None" not in extracted:
        if matches and "None" not in matches:
            for match in matches:
                search_tasks.append(perform_similarity_search(collection, match))
        else:
            print("Requested course(s) are not valid.")
            return [], None, None

    elif previous_matches:
        print("No matches found for current prompt. Using previous prompt's matches.")
        for match in previous_matches:
            search_tasks.append(perform_similarity_search(collection, match))
    else:
        print("No matches found.")
        return [], None, None

    if search_tasks:
        search_results = await asyncio.gather(*search_tasks)
        for documents, metadatas in search_results:
            if documents:
                for i, doc in enumerate(documents):
                    metadata_list.append(metadatas[i])
                    all_results.append({
                        "document": doc,
                        "metadata": metadatas[i],
                    })

    if metadata_list:
        refined_response = await perform_refined_llama_call(metadata_list, user_prompt)

    return all_results, matches, refined_response



async def main():
    previous_matches = None
    while True:
        user_prompt = input("\nEnter your prompt (or 'exit'): \n")
        if user_prompt.lower() == "exit":
            break

        results, current_matches, refined_response = await process_query(user_prompt, previous_matches)
        if current_matches and "None" not in current_matches:
            previous_matches = current_matches


if __name__ == "__main__":
    asyncio.run(main())