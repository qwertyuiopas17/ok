"""
Sehat Sahara Health Assistant - App Navigator and Symptom Checker
Strictly follows the Sehat Sahara specification for rural Indian users
"""

import json
import logging
import re
from typing import Dict, Any, Optional
from datetime import datetime

class SehatSaharaAssistant:
    """
    Sehat Sahara Assistant - App Navigator and Symptom Checker
    Strictly follows NO MEDICAL ADVICE rule and provides only navigation assistance
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        # Language detection patterns
        self.language_patterns = {
            'hi': [
                r'\b(hai|kya|kaise|kab|kahan|kahan|meri|mera|teri|tera|chahiye|leni|karna|karne|nahi|bhi|par|aur|bukhar|dard|khansi|tabiyat|kharaab|bimari|doctor|appointment|madad|help|namaste|kaun|kaisa|kitna|kabhi|kabhi|bas|aur|ek|do|teen|char|paanch|cheh|saat|aath|nau|das)\b',
            ],
            'pa': [
                r'\b(hai|ki|kive|kado|kithe|meri|mera|teri|tera|chahidi|leni|karna|karne|nahin|bhi|par|aur|bukhar|dukh|khansi|tabiyat|kharaab|bimari|doctor|appointment|madad|help|sat|sri|akal|ki|kinne|kithon|kithe|kivein|bas|ate|ik|do|tin|char|panj|chhe|satt|atth|nau|das)\b',
            ],
            'en': [
                r'\b(the|is|are|do|have|my|i|you|this|that|what|how|when|where|why|fever|headache|pain|cough|cold|doctor|appointment|help|medicine|hello|hi|yes|no|please|thank|thanks|need|want|have|has|had|will|would|can|could|should|take|get|give|make|go|come|see|look|find|book|schedule|appointment|doctor|medicine|health|pain|fever|cough|cold|sick|hurt|ache|problem|issue|help|emergency|urgent)\b'
            ]
        }

        # Symptom keywords for detection
        self.symptom_keywords = {
            'hi': ['bukhar', 'sir dard', 'dard', 'khansi', 'thakan', 'kamzori', 'ulti', 'dast'],
            'pa': ['bukhar', 'sir dukh', 'dukh', 'khansi', 'thakan', 'kamzori', 'ulti', 'dast'],
            'en': ['fever', 'headache', 'pain', 'cough', 'tired', 'weak', 'vomiting', 'diarrhea']
        }

        # Conversation state tracking
        self.conversation_states = {}  # user_id -> state

        # Symptom checker questions by language
        self.symptom_questions = {
            'hi': [
                "मैं आपकी मदद करने के लिए हूं। कृपया अपने लक्षणों के बारे में बताएं।",
                "आपको क्या परेशानी हो रही है?",
                "कितने समय से आपको ये समस्या है?",
                "दर्द की तीव्रता 1 से 10 के बीच कितनी है?",
                "क्या आपको बुखार, खांसी या कोई अन्य समस्या भी है?",
                "क्या आपका पेट खराब है या उल्टी हो रही है?",
                "क्या आपको सांस लेने में कोई दिक्कत है?",
                "क्या आपको सीने में दर्द है?"
            ],
            'pa': [
                "ਮੈਂ ਤੁਹਾਡੀ ਮਦਦ ਕਰਨ ਲਈ ਹਾਂ। ਕਿਰਪਾ ਕਰਕੇ ਆਪਣੇ ਲੱਛਣਾਂ ਬਾਰੇ ਦੱਸੋ।",
                "ਤੁਹਾਨੂੰ ਕੀ ਪਰੇਸ਼ਾਨੀ ਹੋ ਰਹੀ ਹੈ?",
                "ਕਿੰਨੇ ਸਮੇਂ ਤੋਂ ਤੁਹਾਨੂੰ ਇਹ ਸਮੱਸਿਆ ਹੈ?",
                "ਦਰਦ ਦੀ ਤੀਬਰਤਾ 1 ਤੋਂ 10 ਵਿੱਚੋਂ ਕਿੰਨੀ ਹੈ?",
                "ਕੀ ਤੁਹਾਨੂੰ ਬੁਖ਼ਾਰ, ਖੰਘ ਜਾਂ ਕੋਈ ਹੋਰ ਸਮੱਸਿਆ ਵੀ ਹੈ?",
                "ਕੀ ਤੁਹਾਡਾ ਪੇਟ ਖ਼ਰਾਬ ਹੈ ਜਾਂ ਉਲਟੀ ਹੋ ਰਹੀ ਹੈ?",
                "ਕੀ ਤੁਹਾਨੂੰ ਸਾਹ ਲੈਣ ਵਿੱਚ ਕੋਈ ਦਿੱਕਤ ਹੈ?",
                "ਕੀ ਤੁਹਾਨੂੰ ਸੀਨੇ ਵਿੱਚ ਦਰਦ ਹੈ?"
            ],
            'en': [
                "I am here to help. Please tell me about your symptoms.",
                "What is troubling you?",
                "How long have you been feeling this way?",
                "On a scale of 1 to 10, how severe is the pain?",
                "Are you experiencing any fever, cough or any other issues?",
                "Are you having stomach problems or vomiting?",
                "Are you having any difficulty breathing?",
                "Are you experiencing chest pain?"
            ]
        }

        # Precautionary advice by language (general only, no medical advice)
        self.precautionary_advice = {
            'hi': {
                'fever': "आराम करें और खूब पानी पीएं। मच्छरदानी का इस्तेमाल करें।",
                'cough': "गर्म पानी के साथ नमक से गरारे करें। अदरक वाली चाय पीएं।",
                'stomach': "सादा खाना जैसे खिचड़ी खाएं। ORS घोल पीएं।",
                'general': "आराम करें और खूब तरल पदार्थ पीएं।"
            },
            'pa': {
                'fever': "ਆਰਾਮ ਕਰੋ ਅਤੇ ਖੂਬ ਪਾਣੀ ਪੀਓ। ਮੱਛਰਦਾਨੀ ਦਾ ਇਸਤੇਮਾਲ ਕਰੋ।",
                'cough': "ਗਰਮ ਪਾਣੀ ਨਾਲ ਨਮਕ ਨਾਲ ਗਰਾਰੇ ਕਰੋ। ਅਦਰਕ ਵਾਲੀ ਚਾਹ ਪੀਓ।",
                'stomach': "ਸਾਦਾ ਖਾਣਾ ਜਿਵੇਂ ਖਿਚੜੀ ਖਾਓ। ORS ਘੋਲ ਪੀਓ।",
                'general': "ਆਰਾਮ ਕਰੋ ਅਤੇ ਖੂਬ ਤਰਲ ਪਦਾਰਥ ਪੀਓ।"
            },
            'en': {
                'fever': "Get plenty of rest and stay hydrated by drinking water or fluids.",
                'cough': "Gargle with warm salt water or drink warm fluids like ginger tea.",
                'stomach': "Eat simple, light foods like khichdi and drink plenty of fluids like ORS.",
                'general': "Get plenty of rest and stay hydrated."
            }
        }

    def detect_language(self, message: str) -> str:
        """Detect language from message using keyword patterns and script detection"""
        if not message or not message.strip():
            return 'en'

        message_lower = message.lower().strip()

        # Script-based detection (highest priority)
        if re.search(r'[\u0900-\u097F]', message):  # Devanagari
            return 'hi'
        elif re.search(r'[\u0A00-\u0A7F]', message):  # Gurmukhi
            return 'pa'

        # Keyword-based detection
        scores = {'hi': 0, 'pa': 0, 'en': 0}

        for lang, patterns in self.language_patterns.items():
            for pattern in patterns:
                if re.search(pattern, message_lower, re.IGNORECASE):
                    scores[lang] += 1

        # Return language with highest score
        if max(scores.values()) > 0:
            return max(scores, key=scores.get)
        else:
            return 'en'  # Default fallback

    def get_conversation_state(self, user_id: str) -> Dict[str, Any]:
        """Get or initialize conversation state for user"""
        if user_id not in self.conversation_states:
            self.conversation_states[user_id] = {
                'language': 'en',
                'stage': 'initial',
                'symptom_count': 0,
                'symptoms_gathered': [],
                'last_question': None
            }
        return self.conversation_states[user_id]

    def update_conversation_state(self, user_id: str, **updates):
        """Update conversation state for user"""
        state = self.get_conversation_state(user_id)
        state.update(updates)
        self.conversation_states[user_id] = state

    def is_emergency_detected(self, message: str, language: str) -> bool:
        """Check if message indicates emergency situation"""
        emergency_keywords = {
            'hi': ['emergency', 'accident', 'ambulance', 'turant', 'jaldi', 'madad', 'seene mein dard', 'saans nahi aa rahi', 'bahut tez dard', 'dil ka dora', 'heart attack', 'behosh', 'unconscious', 'khoon', 'bleeding', 'mar raha', 'dying'],
            'pa': ['emergency', 'accident', 'ambulance', 'turant', 'jaldi', 'madad', 'seene vich dard', 'saans nahi aa rahi', 'bahut tez dard', 'dil da dora', 'heart attack', 'behosh', 'unconscious', 'khoon', 'bleeding', 'mar raha', 'dying'],
            'en': ['emergency', 'accident', 'ambulance', 'urgent', 'help', 'chest pain', 'cannot breathe', 'severe pain', 'heart attack', 'unconscious', 'bleeding', 'dying']
        }

        message_lower = message.lower()
        keywords = emergency_keywords.get(language, emergency_keywords['en'])

        return any(keyword in message_lower for keyword in keywords)

    def process_message(self, message: str, user_id: str = "default") -> Dict[str, Any]:
        """
        Process user message and return Sehat Sahara response in exact JSON format
        This is the main entry point that follows the strict specification
        """
        try:
            # Detect language from first message if this is initial contact
            state = self.get_conversation_state(user_id)

            if state['stage'] == 'initial':
                detected_language = self.detect_language(message)
                state['language'] = detected_language
                self.update_conversation_state(user_id, language=detected_language, stage='understanding')

            language = state['language']

            # Check for emergency
            if self.is_emergency_detected(message, language):
                return self._create_response(
                    language=language,
                    response=self._get_emergency_message(language),
                    action="TRIGGER_SOS",
                    parameters={"emergency_number": "108", "type": "medical_emergency"}
                )

            # Check if asking for medical advice (forbidden)
            if self._is_medical_advice_request(message, language):
                return self._create_response(
                    language=language,
                    response=self._get_no_medical_advice_message(language),
                    action="Maps_TO_APPOINTMENT_BOOKING",
                    parameters={}
                )

            # Handle conversation flow based on current stage
            if state['stage'] == 'symptom_check':
                return self._handle_symptom_check(message, user_id, language)
            else:
                return self._handle_initial_inquiry(message, user_id, language)

        except Exception as e:
            self.logger.error(f"Error processing message: {e}")
            return self._create_response(
                language='en',
                response="I'm having trouble understanding. Let me connect you with a support agent.",
                action="CONNECT_TO_SUPPORT_AGENT",
                parameters={"reason": "system_error"}
            )

    def _handle_initial_inquiry(self, message: str, user_id: str, language: str) -> Dict[str, Any]:
        """Handle initial user inquiry"""
        # Check if user is describing symptoms
        symptoms_detected = self._detect_symptoms(message, language)

        if symptoms_detected:
            # Start symptom checker flow
            self.update_conversation_state(user_id, stage='symptom_check', symptom_count=1, symptoms_gathered=symptoms_detected)
            return self._create_response(
                language=language,
                response=self._get_next_symptom_question(user_id, language),
                action="CONTINUE_SYMPTOM_CHECK",
                parameters={}
            )
        else:
            # General inquiry - offer help
            return self._create_response(
                language=language,
                response=self._get_general_help_message(language),
                action="SHOW_APP_FEATURES",
                parameters={}
            )

    def _handle_symptom_check(self, message: str, user_id: str, language: str) -> Dict[str, Any]:
        """Handle symptom checking conversation flow"""
        state = self.get_conversation_state(user_id)

        # Add user input to symptoms gathered
        current_symptoms = state.get('symptoms_gathered', [])
        new_symptoms = self._detect_symptoms(message, language)
        all_symptoms = list(set(current_symptoms + new_symptoms))

        # Update state
        self.update_conversation_state(
            user_id,
            symptom_count=state['symptom_count'] + 1,
            symptoms_gathered=all_symptoms
        )

        # Check if we have enough information (3-4 exchanges)
        if state['symptom_count'] >= 3:
            # Provide precautions and recommend doctor consultation
            return self._provide_precautions_and_recommend_doctor(user_id, language, all_symptoms)
        else:
            # Continue asking questions
            return self._create_response(
                language=language,
                response=self._get_next_symptom_question(user_id, language),
                action="CONTINUE_SYMPTOM_CHECK",
                parameters={}
            )

    def _provide_precautions_and_recommend_doctor(self, user_id: str, language: str, symptoms: list) -> Dict[str, Any]:
        """Provide general precautions and recommend doctor consultation"""
        # Get appropriate precautions based on symptoms
        precautions = self._get_precautions_for_symptoms(symptoms, language)

        # Create response with mandatory disclaimer
        response_text = f"{precautions}\n\n{self._get_disclaimer_message(language)}"

        # Reset conversation state for next interaction
        self.update_conversation_state(user_id, stage='initial', symptom_count=0, symptoms_gathered=[])

        return self._create_response(
            language=language,
            response=response_text,
            action="Maps_TO_APPOINTMENT_BOOKING",
            parameters={}
        )

    def _detect_symptoms(self, message: str, language: str) -> list:
        """Detect symptoms mentioned in message"""
        symptoms_found = []
        keywords = self.symptom_keywords.get(language, [])

        message_lower = message.lower()
        for keyword in keywords:
            if keyword in message_lower:
                symptoms_found.append(keyword)

        return symptoms_found

    def _get_next_symptom_question(self, user_id: str, language: str) -> str:
        """Get next question in symptom checker flow"""
        state = self.get_conversation_state(user_id)
        questions = self.symptom_questions.get(language, self.symptom_questions['en'])
        question_index = min(state['symptom_count'], len(questions) - 1)

        question = questions[question_index]
        self.update_conversation_state(user_id, last_question=question)

        return question

    def _get_precautions_for_symptoms(self, symptoms: list, language: str) -> str:
        """Get general precautions based on detected symptoms"""
        advice = self.precautionary_advice.get(language, self.precautionary_advice['en'])

        if not symptoms:
            return advice['general']

        # Map symptoms to advice categories
        symptom_to_category = {
            'bukhar': 'fever',
            'fever': 'fever',
            'khansi': 'cough',
            'cough': 'cough',
            'dast': 'stomach',
            'stomach': 'stomach',
            'ulti': 'stomach',
            'vomiting': 'stomach'
        }

        # Get most relevant advice
        for symptom in symptoms:
            category = symptom_to_category.get(symptom)
            if category and category in advice:
                return advice[category]

        return advice['general']

    def _is_medical_advice_request(self, message: str, language: str) -> bool:
        """Check if user is asking for medical advice (forbidden)"""
        medical_advice_keywords = {
            'hi': ['kya dawai', 'kaun si dawai', 'ilaj kya', 'kaise theek', 'diagnosis', 'medicine', 'tablet', 'dawai', 'capsule', 'injection', 'dose', 'kitni dawai', 'kab dawai', 'kaise khana', 'side effect', 'allergy'],
            'pa': ['ki dawai', 'kihri dawai', 'ilaj ki', 'kivein theek', 'diagnosis', 'medicine', 'tablet', 'dawai', 'capsule', 'injection', 'dose', 'kinni dawai', 'kad dawai', 'kivein khana', 'side effect', 'allergy'],
            'en': ['what medicine', 'which tablet', 'how to cure', 'what treatment', 'diagnosis', 'medicine', 'tablet', 'capsule', 'injection', 'dose', 'how much', 'when to take', 'side effect', 'allergy']
        }

        message_lower = message.lower()
        keywords = medical_advice_keywords.get(language, medical_advice_keywords['en'])

        return any(keyword in message_lower for keyword in keywords)

    def _get_emergency_message(self, language: str) -> str:
        """Get emergency response message"""
        messages = {
            'hi': "यह आपातकालीन स्थिति है। मैं आपको तुरंत आपातकालीन सेवाओं से जोड़ रही हूं। एंबुलेंस के लिए 108 कॉल करें।",
            'pa': "ਇਹ ਐਮਰਜੈਂਸੀ ਸਥਿਤੀ ਹੈ। ਮੈਂ ਤੁਹਾਨੂੰ ਤੁਰੰਤ ਐਮਰਜੈਂਸੀ ਸੇਵਾਵਾਂ ਨਾਲ ਜੋੜ੍ਹ ਰਹੀ ਹਾਂ। ਐਂਬੂਲੈਂਸ ਲਈ 108 ਕਾਲ ਕਰੋ।",
            'en': "This is an emergency situation. I'm connecting you to emergency services immediately. For ambulance, call 108."
        }
        return messages.get(language, messages['en'])

    def _get_no_medical_advice_message(self, language: str) -> str:
        """Get response for medical advice requests"""
        messages = {
            'hi': "मैं डॉक्टर नहीं हूं और निदान नहीं दे सकती। हालांकि, मैं आपको अभी एक qualified डॉक्टर के साथ appointment बुक करने में मदद कर सकती हूं जो आपको सही सलाह दे सके। क्या आप आगे बढ़ना चाहेंगे?",
            'pa': "ਮੈਂ ਡਾਕਟਰ ਨਹੀਂ ਹਾਂ ਅਤੇ ਨਿਦਾਨ ਨਹੀਂ ਦੇ ਸਕਦੀ। ਹਾਲਾਂਕਿ, ਮੈਂ ਤੁਹਾਨੂੰ ਹੁਣੇ ਇੱਕ qualified ਡਾਕਟਰ ਨਾਲ appointment ਬੁਕ ਕਰਨ ਵਿੱਚ ਮਦਦ ਕਰ ਸਕਦੀ ਹਾਂ ਜੋ ਤੁਹਾਨੂੰ ਸਹੀ ਸਲਾਹ ਦੇ ਸਕੇ। ਕੀ ਤੁਸੀਂ ਅੱਗੇ ਵਧਣਾ ਚਾਹੋਗੇ?",
            'en': "I am not a doctor and cannot provide a diagnosis. However, I can help you book an appointment with a qualified doctor right now who can give you the correct advice. Would you like to proceed?"
        }
        return messages.get(language, messages['en'])

    def _get_general_help_message(self, language: str) -> str:
        """Get general help message"""
        messages = {
            'hi': "मैं Sehat Sahara ऐप में आपकी मदद करने के लिए हूं। मैं आपकी मदद कर सकती हूं appointment बुक करने, दवाइयों की जानकारी ढूंढने, health records चेक करने और भी बहुत कुछ में। आप क्या मदद चाहते हैं?",
            'pa': "ਮੈਂ Sehat Sahara ਐਪ ਵਿੱਚ ਤੁਹਾਡੀ ਮਦਦ ਕਰਨ ਲਈ ਹਾਂ। ਮੈਂ ਤੁਹਾਡੀ ਮਦਦ ਕਰ ਸਕਦੀ ਹਾਂ appointment ਬੁਕ ਕਰਨ, ਦਵਾਈਆਂ ਦੀ ਜਾਣਕਾਰੀ ਲੱਭਣ, health records ਚੈਕ ਕਰਨ ਅਤੇ ਵੀ ਬਹੁਤ ਕੁਝ ਵਿੱਚ। ਤੁਸੀਂ ਕੀ ਮਦਦ ਚਾਹੁੰਦੇ ਹੋ?",
            'en': "I'm here to help you navigate the Sehat Sahara app. I can help you book appointments, find medicine information, check health records, and more. What would you like help with?"
        }
        return messages.get(language, messages['en'])

    def _get_disclaimer_message(self, language: str) -> str:
        """Get mandatory disclaimer message"""
        messages = {
            'hi': "कृपया याद रखें, यह चिकित्सा सलाह या निदान नहीं है। उचित इलाज के लिए डॉक्टर से परामर्श करना बहुत जरूरी है। क्या आप अभी appointment बुक करना चाहेंगे?",
            'pa': "ਕਿਰਪਾ ਕਰਕੇ ਯਾਦ ਰੱਖੋ, ਇਹ ਦਵਾਈ ਸਲਾਹ ਜਾਂ ਨਿਦਾਨ ਨਹੀਂ ਹੈ। ਉਚਿਤ ਇਲਾਜ ਲਈ ਡਾਕਟਰ ਨਾਲ ਸਲਾਹ ਕਰਨਾ ਬਹੁਤ ਜ਼ਰੂਰੀ ਹੈ। ਕੀ ਤੁਸੀਂ ਹੁਣੇ appointment ਬੁਕ ਕਰਨਾ ਚਾਹੋਗੇ?",
            'en': "Please remember, this is not medical advice or a diagnosis. For proper treatment, it is very important to consult with a doctor. Would you like me to help you book an appointment now?"
        }
        return messages.get(language, messages['en'])

    def _create_response(self, language: str, response: str, action: str, parameters: Dict) -> Dict[str, Any]:
        """Create response in exact JSON format specified"""
        return {
            "language": language,
            "response": response,
            "action": action,
            "parameters": parameters
        }

    def reset_conversation(self, user_id: str):
        """Reset conversation state for user"""
        if user_id in self.conversation_states:
            del self.conversation_states[user_id]

    def get_supported_languages(self) -> list:
        """Get list of supported languages"""
        return ['hi', 'pa', 'en']