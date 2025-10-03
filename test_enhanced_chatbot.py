#!/usr/bin/env python3
"""
Comprehensive test script for enhanced Sehat Sahara chatbot functionality
Tests all new features: interactive buttons, progress tracking, post-appointment follow-up, etc.
"""

import sys
import os
import json
import logging
from datetime import datetime, timedelta

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ko import ProgressiveResponseGenerator
from nlu_processor import ProgressiveNLUProcessor
from conversation_memory import ProgressiveConversationMemory

def setup_logging():
    """Setup logging for testing"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def test_progress_tracking():
    """Test appointment progress tracking"""
    print("\n" + "=" * 60)
    print("TESTING PROGRESS TRACKING")
    print("=" * 60)

    memory = ProgressiveConversationMemory()
    user_id = "test_progress_user"

    # Simulate appointment booking
    appointment_id = "APT001"
    appointment_date = datetime.now() + timedelta(days=1)

    memory.update_appointment_status(
        user_id=user_id,
        appointment_id=appointment_id,
        status="booked",
        appointment_date=appointment_date
    )

    # Mark as completed
    memory.update_appointment_status(
        user_id=user_id,
        appointment_id=appointment_id,
        status="completed",
        appointment_date=appointment_date
    )

    # Get progress summary
    progress = memory.get_user_progress_summary(user_id)
    print(f"Appointments booked: {progress.get('appointments_booked', 0)}")
    print(f"Appointments completed: {progress.get('appointments_completed', 0)}")
    print(f"Feedback pending: {progress.get('feedback_pending', False)}")

def test_prescription_summarization():
    """Test prescription summarization"""
    print("\n" + "=" * 60)
    print("TESTING PRESCRIPTION SUMMARIZATION")
    print("=" * 60)

    memory = ProgressiveConversationMemory()
    user_id = "test_prescription_user"

    # Add sample prescription
    prescription_data = {
        'doctor_name': 'Dr. Sharma',
        'medications': [
            {'name': 'Paracetamol', 'dosage': '500mg', 'frequency': 'twice daily'},
            {'name': 'Cough Syrup', 'dosage': '10ml', 'frequency': 'three times daily'},
            {'name': 'Vitamin C', 'dosage': '1000mg', 'frequency': 'once daily'}
        ],
        'diagnosis': 'Common Cold',
        'instructions': 'Take rest and drink plenty of fluids'
    }

    memory.add_prescription_summary(user_id, prescription_data)

    # Get prescription summary
    summary = memory.get_prescription_summary(user_id)
    print(f"Doctor: {summary.get('doctor_name', 'N/A')}")
    print(f"Medications count: {len(summary.get('medications', []))}")
    print(f"Diagnosis: {summary.get('diagnosis', 'N/A')}")

    # Test response generator
    response_gen = ProgressiveResponseGenerator()
    summary_response = response_gen.generate_prescription_summary_response(prescription_data, 'en')
    print(f"Summary response length: {len(summary_response)} characters")

def test_post_appointment_followup():
    """Test post-appointment follow-up logic"""
    print("\n" + "=" * 60)
    print("TESTING POST-APPOINTMENT FOLLOW-UP")
    print("=" * 60)

    memory = ProgressiveConversationMemory()
    user_id = "test_followup_user"

    # Set up completed appointment
    appointment_date = datetime.now() - timedelta(days=2)  # 2 days ago
    memory.update_appointment_status(
        user_id=user_id,
        appointment_id="APT002",
        status="completed",
        appointment_date=appointment_date
    )

    # Check if follow-up is needed
    followup = memory.check_post_appointment_followup(user_id)
    print(f"Follow-up needed: {followup.get('needed', False)}")
    if followup.get('needed'):
        print(f"Days since appointment: {followup.get('days_since', 0)}")

def test_interactive_buttons():
    """Test interactive button system"""
    print("\n" + "=" * 60)
    print("TESTING INTERACTIVE BUTTONS")
    print("=" * 60)

    response_gen = ProgressiveResponseGenerator()
    user_id = "test_button_user"

    # Test appointment booking intent
    buttons = response_gen._get_interactive_buttons('appointment_booking', 'en', {})
    print(f"Appointment booking buttons: {len(buttons)}")
    if buttons:
        print(f"Button text: {buttons[0].get('text', 'N/A')}")
        print(f"Button action: {buttons[0].get('action', 'N/A')}")

    # Test medicine scan intent
    buttons = response_gen._get_interactive_buttons('medicine_scan', 'hi', {})
    print(f"Medicine scan buttons (Hindi): {len(buttons)}")
    if buttons:
        button_text = buttons[0].get('text', 'N/A')
        print(f"Button text: {button_text.encode('ascii', 'ignore').decode('ascii', 'ignore')}")

    # Test emergency intent
    buttons = response_gen._get_interactive_buttons('emergency_assistance', 'pa', {})
    print(f"Emergency buttons (Punjabi): {len(buttons)}")
    if buttons:
        button_text = buttons[0].get('text', 'N/A')
        print(f"Button text: {button_text.encode('ascii', 'ignore').decode('ascii', 'ignore')}")

def test_feature_guidance():
    """Test feature guidance in responses"""
    print("\n" + "=" * 60)
    print("TESTING FEATURE GUIDANCE")
    print("=" * 60)

    response_gen = ProgressiveResponseGenerator()

    # Test medicine scan guidance
    test_response = "I can help you scan your medicine."
    enhanced_response = response_gen._add_feature_guidance(test_response, 'medicine_scan', 'en')

    print(f"Original response length: {len(test_response)}")
    print(f"Enhanced response length: {len(enhanced_response)}")
    print(f"Contains guidance: {'💡' in enhanced_response}")

    # Test Hindi guidance
    enhanced_hindi = response_gen._add_feature_guidance(test_response, 'medicine_scan', 'hi')
    print(f"Hindi guidance included: {'💡' in enhanced_hindi}")

def test_enhanced_nlu():
    """Test enhanced NLU with new intents"""
    print("\n" + "=" * 60)
    print("TESTING ENHANCED NLU")
    print("=" * 60)

    nlu_proc = ProgressiveNLUProcessor()

    # Test new intents
    test_messages = [
        ("feeling better after appointment", "post_appointment_followup"),
        ("what did doctor prescribe", "prescription_summary_request"),
        ("appointment was good", "post_appointment_followup"),
        ("show me my medicines", "prescription_summary_request")
    ]

    for message, expected_intent in test_messages:
        result = nlu_proc.understand_user_intent(message, sehat_sahara_mode=True)
        detected_intent = result.get('primary_intent', 'unknown')
        confidence = result.get('confidence', 0)

        status = "PASS" if expected_intent in detected_intent else "FAIL"
        print(f"{status} '{message}' -> {detected_intent} (confidence: {confidence:.2f})")

def test_enhanced_response_generator():
    """Test enhanced response generator with Sehat Sahara mode"""
    print("\n" + "=" * 60)
    print("TESTING ENHANCED RESPONSE GENERATOR")
    print("=" * 60)

    response_gen = ProgressiveResponseGenerator()
    nlu_proc = ProgressiveNLUProcessor()

    # Test new intents with Sehat Sahara mode
    test_cases = [
        ("appointment book karni hai", "appointment_booking"),
        ("feeling better after appointment", "post_appointment_followup"),
        ("what did doctor prescribe", "prescription_summary_request")
    ]

    for message, expected_intent in test_cases:
        nlu_result = nlu_proc.understand_user_intent(message, sehat_sahara_mode=True)
        response = response_gen.generate_response(
            user_message=message,
            nlu_result=nlu_result,
            sehat_sahara_mode=True
        )

        print(f"\nMessage: {message}")
        print(f"Intent: {nlu_result.get('primary_intent', 'unknown')}")
        print(f"Response action: {response.get('action', 'unknown')}")
        print(f"Has interactive buttons: {'interactive_buttons' in response}")
        print(f"Language: {response.get('language', 'unknown')}")

def test_complete_workflow():
    """Test complete workflow with all features"""
    print("\n" + "=" * 60)
    print("TESTING COMPLETE WORKFLOW")
    print("=" * 60)

    memory = ProgressiveConversationMemory()
    response_gen = ProgressiveResponseGenerator()
    nlu_proc = ProgressiveNLUProcessor()

    user_id = "test_workflow_user"

    # Simulate complete user journey
    workflow_messages = [
        "Namaste, mujhe bukhar hai",  # Initial symptom
        "do din se",  # Duration
        "haan, khansi bhi hai",  # Additional symptoms
        "appointment book karni hai",  # Request appointment
        "appointment was good",  # Post-appointment feedback
        "what did doctor prescribe"  # Request prescription summary
    ]

    for i, message in enumerate(workflow_messages, 1):
        print(f"\n--- Turn {i} ---")
        print(f"User: {message}")

        # Process with NLU
        nlu_result = nlu_proc.understand_user_intent(message, sehat_sahara_mode=True)

        # Generate response
        response = response_gen.generate_response(
            user_message=message,
            nlu_result=nlu_result,
            sehat_sahara_mode=True
        )

        # Save to conversation memory
        memory.add_conversation_turn(
            user_id=user_id,
            user_message=message,
            bot_response=json.dumps(response),
            nlu_result=nlu_result
        )

        print(f"Bot: {response.get('response', 'No response')[:100]}...")
        print(f"Action: {response.get('action', 'No action')}")
        print(f"Buttons: {len(response.get('interactive_buttons', []))}")


def run_all_tests():
    """Run all enhanced functionality tests"""
    setup_logging()

    print("ENHANCED SEHAT SAHARA CHATBOT - COMPREHENSIVE TEST SUITE")
    print("=" * 80)

    try:
        test_progress_tracking()
        test_prescription_summarization()
        test_post_appointment_followup()
        test_interactive_buttons()
        test_feature_guidance()
        test_enhanced_nlu()
        test_enhanced_response_generator()
        test_complete_workflow()

        print("\n" + "=" * 80)
        print("✅ ALL ENHANCED TESTS COMPLETED")
        print("=" * 80)

    except Exception as e:
        print(f"\nFAILED ENHANCED TEST SUITE: {str(e)[:100]}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_all_tests()