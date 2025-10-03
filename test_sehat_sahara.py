#!/usr/bin/env python3
"""
Test script for Sehat Sahara Assistant
Tests the implementation with various sample conversations
"""

import sys
import os
import json
import logging

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sehat_sahara_assistant import SehatSaharaAssistant

def setup_logging():
    """Setup logging for testing"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def test_language_detection():
    """Test language detection functionality"""
    print("=" * 60)
    print("TESTING LANGUAGE DETECTION")
    print("=" * 60)

    assistant = SehatSaharaAssistant()

    test_messages = [
        ("bukhar hai", "hi"),
        ("mere sir mein dard hai", "hi"),
        ("I have fever", "en"),
        ("I have headache", "en"),
        ("appointment book karni hai", "hi"),
        ("need to book appointment", "en"),
        ("doctor se milna hai", "hi"),
        ("fever and cough", "en")
    ]

    for message, expected_lang in test_messages:
        detected_lang = assistant.detect_language(message)
        status = "PASS" if detected_lang == expected_lang else "FAIL"
        print(f"{status} '{message}' -> {detected_lang} (expected: {expected_lang})")

def test_emergency_detection():
    """Test emergency situation detection"""
    print("\n" + "=" * 60)
    print("TESTING EMERGENCY DETECTION")
    print("=" * 60)

    assistant = SehatSaharaAssistant()

    emergency_messages = [
        ("seene mein dard ho raha hai", "hi"),
        ("chest pain emergency", "en"),
        ("accident hua hai", "hi"),
        ("having accident", "en"),
        ("bahut tez dard hai", "hi"),
        ("severe pain", "en")
    ]

    normal_messages = [
        ("bukhar hai", "hi"),
        ("I have fever", "en"),
        ("appointment book karni hai", "hi"),
        ("need appointment", "en")
    ]

    print("Emergency messages:")
    for message, lang in emergency_messages:
        is_emergency = assistant.is_emergency_detected(message, lang)
        status = "PASS" if is_emergency else "FAIL"
        print(f"{status} '{message}' -> Emergency: {is_emergency}")

    print("\nNormal messages:")
    for message, lang in normal_messages:
        is_emergency = assistant.is_emergency_detected(message, lang)
        status = "PASS" if not is_emergency else "FAIL"
        print(f"{status} '{message}' -> Emergency: {is_emergency}")

def test_medical_advice_detection():
    """Test medical advice request detection"""
    print("\n" + "=" * 60)
    print("TESTING MEDICAL ADVICE DETECTION")
    print("=" * 60)

    assistant = SehatSaharaAssistant()

    medical_advice_requests = [
        ("kya dawai loon?", "hi"),
        ("what medicine should I take?", "en"),
        ("kaun si dawai acchi hai?", "hi"),
        ("which tablet is good?", "en"),
        ("ilaj kya hai?", "hi"),
        ("what is the treatment?", "en")
    ]

    normal_requests = [
        ("appointment book karni hai", "hi"),
        ("need to see doctor", "en"),
        ("muje doctor se milna hai", "hi"),
        ("doctor appointment chahiye", "hi")
    ]

    print("Medical advice requests:")
    for message, lang in medical_advice_requests:
        is_medical_advice = assistant._is_medical_advice_request(message, lang)
        status = "PASS" if is_medical_advice else "FAIL"
        print(f"{status} '{message}' -> Medical advice: {is_medical_advice}")

    print("\nNormal requests:")
    for message, lang in normal_requests:
        is_medical_advice = assistant._is_medical_advice_request(message, lang)
        status = "PASS" if not is_medical_advice else "FAIL"
        print(f"{status} '{message}' -> Medical advice: {is_medical_advice}")

def test_conversation_flows():
    """Test complete conversation flows"""
    print("\n" + "=" * 60)
    print("TESTING CONVERSATION FLOWS")
    print("=" * 60)

    assistant = SehatSaharaAssistant()

    # Test Hindi conversation flow
    print("Hindi Conversation Flow:")
    user_id = "test_user_hindi"

    messages = [
        "Namaste, mujhe bukhar hai",
        "do din se",
        "haan, khansi bhi hai",
        "nahi, seene mein dard nahi hai"
    ]

    for i, message in enumerate(messages, 1):
        response = assistant.process_message(message, user_id)
        print(f"\nTurn {i}:")
        print(f"User: {message}")
        print(f"Assistant: {json.dumps(response, ensure_ascii=True, indent=2)}")

    # Test English conversation flow
    print("\n" + "English Conversation Flow:")
    user_id = "test_user_english"

    messages = [
        "Hello, I have fever",
        "Since yesterday",
        "Yes, I also have cough",
        "No chest pain"
    ]

    for i, message in enumerate(messages, 1):
        response = assistant.process_message(message, user_id)
        print(f"\nTurn {i}:")
        print(f"User: {message}")
        print(f"Assistant: {json.dumps(response, ensure_ascii=False, indent=2)}")

    for i, message in enumerate(messages, 1):
        response = assistant.process_message(message, user_id)
        print(f"\nTurn {i}:")
        print(f"User: {message}")
        print(f"Assistant: {json.dumps(response, ensure_ascii=False, indent=2)}")

def test_emergency_flow():
    """Test emergency situation handling"""
    print("\n" + "=" * 60)
    print("TESTING EMERGENCY FLOW")
    print("=" * 60)

    assistant = SehatSaharaAssistant()

    emergency_messages = [
        ("seene mein dard ho raha hai", "hi"),
        ("chest pain emergency", "en")
    ]

    for message, lang in emergency_messages:
        response = assistant.process_message(message, "emergency_user")
        print(f"\nEmergency message: {message}")
        print(f"Response: {json.dumps(response, ensure_ascii=True, indent=2)}")

def test_medical_advice_flow():
    """Test medical advice request handling"""
    print("\n" + "=" * 60)
    print("TESTING MEDICAL ADVICE FLOW")
    print("=" * 60)

    assistant = SehatSaharaAssistant()

    medical_advice_requests = [
        ("kya dawai loon?", "hi"),
        ("what medicine should I take?", "en")
    ]

    for message, lang in medical_advice_requests:
        response = assistant.process_message(message, "advice_user")
        print(f"\nMedical advice request: {message}")
        print(f"Response: {json.dumps(response, ensure_ascii=True, indent=2)}")

def run_all_tests():
    """Run all tests"""
    setup_logging()

    print("SEHAT SAHARA ASSISTANT - COMPREHENSIVE TEST SUITE")
    print("=" * 80)

    try:
        test_language_detection()
        test_emergency_detection()
        test_medical_advice_detection()
        test_conversation_flows()
        test_emergency_flow()
        test_medical_advice_flow()

        print("\n" + "=" * 80)
        print("ALL TESTS COMPLETED")
        print("=" * 80)

    except Exception as e:
        print(f"\nFAILED TEST SUITE: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_all_tests()