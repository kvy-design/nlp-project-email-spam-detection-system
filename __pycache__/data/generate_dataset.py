import os
import random
import pandas as pd

# Define realistic email templates and sample texts across all 3 categories

LEGITIMATE_SAMPLES = [
    "Hi team, just a reminder about our project sync scheduled for tomorrow at 10 AM. Please update your slide decks.",
    "Dear Professor, I have attached the revised draft of our research paper on natural language processing for your review.",
    "Hey Kavya, are we still meeting for lunch at the cafeteria today around 1 PM? Let me know!",
    "Your weekly GitHub digest: 5 pull requests merged, 2 issues closed in the repository repository-nlp.",
    "Attached is the monthly utility electricity bill for your residential connection. Total due: $84.20 by next Friday.",
    "Thank you for attending today's lecture on deep neural networks. Please find the lecture notes and references attached.",
    "Hi Sarah, could you please review the pull request for the authentication service before we merge it to master?",
    "Dear Customer, your order #89218 from Amazon has been dispatched and is expected to arrive by Thursday afternoon.",
    "Meeting minutes: We finalized the sprint roadmap for Q4. Action items have been assigned to team members in Jira.",
    "Hey, thanks for sharing the notes from yesterday's conference! The keynote on transformer architectures was great.",
    "Your appointment with Dr. Robert at City Health Clinic is confirmed for Tuesday at 3:30 PM. Please arrive 10 minutes early.",
    "Please find attached the financial report and revenue summary for the third quarter as requested by the board.",
    "Hi everyone, the office will remain closed on Monday for the national holiday. Have a wonderful weekend!",
    "Can you please resend the spreadsheet from last week? I cannot open the corrupted attachment on my desktop.",
    "Flight confirmation: Your flight to Chicago departs at 7:45 AM from Terminal 2. Check-in opens 24 hours prior.",
    "Dear candidate, thank you for interviewing with our engineering team. We would like to invite you for a technical discussion.",
    "Hey! Don't forget that the book club discussion starts at 6 PM on Saturday. We are covering chapters 4 through 7.",
    "Your Google Calendar notification: 'Sprint Retrospective & Planning' starts in 15 minutes.",
    "Good morning team, the CI/CD pipeline has completed building the staging release. Staging environment is ready for testing.",
    "Hi mom, I reached safely and checked into the hotel. The conference starts tomorrow morning. Will call you tonight!",
    "Here is the code review feedback for the database migration script. Please address the indexing comments.",
    "Your subscription receipt for Spotify Premium has been generated. Payment of $9.99 was successfully processed.",
    "Dear student, the deadline for submitting the mini-project documentation has been extended to Friday 5 PM.",
    "The software license renewal for PyCharm Professional has been approved by your department administrator.",
    "Hey Dave, do you have time for a quick 10-minute huddle regarding the client demo tomorrow morning?",
    "Attached are the quarterly lab test results and sensor calibration data for the robotics laboratory experiment.",
    "Hi Alex, great presentation today on natural language feature engineering. Could you share the reference links?",
    "Your ride with Uber has completed. Total charged: $14.50. Thank you for riding with us.",
    "Reminder: Team pizza lunch this Friday in the 4th floor lounge to celebrate our successful project launch!",
    "Dear author, your paper submission has been accepted for presentation at the International NLP Conference.",
    "Hey, let me know if you need help with the machine learning assignment. I finished training the baseline model yesterday.",
    "Your package has been left near the front porch as instructed. Thank you for choosing FedEx delivery service.",
    "Hi Priya, could you verify if the API endpoints are responding correctly after today's deployment?",
    "Attached is the updated project budget spreadsheet reflecting the software licensing costs for this semester.",
    "Notice: Scheduled building power maintenance will occur this Sunday from 2 AM to 6 AM. Elevators will be offline.",
    "Hi team, please find the minutes of our stakeholder discussion attached. Let me know if any updates are needed.",
    "Your monthly bank e-statement for the period ending September 30 is now available to download in your portal.",
    "Hey, are you joining the hackathon this weekend? Our team still needs one more developer for the backend.",
    "Thanks for returning the library books on time. Your borrowing privileges are active through next semester.",
    "Hi everyone, please welcome our new data science intern, Rohan, who will be working with us on NLP tasks."
]

SPAM_SAMPLES = [
    "CONGRATULATIONS! You have been selected as the grand winner of a $1000 Walmart Gift Card! Click here to claim now!",
    "Exclusive Limited Time Offer! Get 85% discount on all designer watches, bags, and luxury accessories. Buy now while stock lasts!",
    "LOSE 20 POUNDS IN 2 WEEKS! No diet, no exercise needed. 100% natural miracle secret formula doctor recommended!",
    "Need urgent cash? Get instant loan approvals up to $50,000 with 0% interest for the first 6 months! No credit check required!",
    "HOT singles in your local neighborhood want to chat with you right now! Join our free dating website today!",
    "Double your Bitcoin in 24 hours! Our automated AI crypto trading robot guarantees 300% weekly returns on investment!",
    "Dear friend, don't miss out on our mega clearance sale. Everything must go! Huge savings across electronics and home appliances.",
    "WIN A FREE BRAND NEW APPLE IPHONE 15 PRO! Fill out this 30-second survey to enter our daily sweepstakes draw!",
    "Earn $500 to $2000 daily working from home for just 2 hours! No prior experience needed. Start immediately!",
    "Eliminate your credit card debt forever! Our certified debt relief experts can cut your debt balance in half today.",
    "Special VIP Casino bonus! Deposit $20 and play with $500 plus 200 free spins on mega jackpot slots!",
    "Increase your website traffic by 1000% with our automated SEO ranking booster tool. Order your package today!",
    "You have unclaimed lottery prize money waiting in your registered name. Reply with your details to receive transfer.",
    "Cheap prescription medications online! Buy Viagra, Cialis, and antibiotics without doctor prescription at discount rates.",
    "FINAL CALL: Your vehicle warranty has expired! Call our toll free number immediately to extend complete coverage.",
    "Turn $100 into $10,000 with this secret binary options trading system. Limited spots available for new investors!",
    "Huge blow-out summer shoe sale! Buy one pair and get two pairs absolutely free. Click now for free shipping worldwide.",
    "Grow your social media following overnight! Buy 10,000 genuine Instagram followers for only $9.99 today!",
    "Congratulations! Your email address won second prize in the UK National Charity Lottery. Claim within 48 hours.",
    "Refinance your mortgage now at historic record-low rates! Save thousands of dollars every month on your home loan.",
    "Unlock all cable TV channels and streaming movies for life with this revolutionary plug-and-play TV stick device!",
    "Special promotional offer: Buy 3 bottles of natural testosterone booster and get 3 bottles free plus express delivery.",
    "You are pre-approved for an exclusive platinum rewards credit card with zero annual fee and unlimited 5% cashback!",
    "Miracle anti-aging skin cream removes wrinkles and fine lines in 3 days! Celebrities love this secret Hollywood formula.",
    "Make fast easy money online taking simple paid consumer surveys! Sign up right now to receive a $50 registration bonus.",
    "Best wholesale dropshipping suppliers directory. Start your profitable e-commerce empire from your bedroom today!",
    "Act now! Clear your tax penalties and IRS back taxes with our guaranteed fresh start tax forgiveness assistance program.",
    "Get rich in real estate with no money down! Attend our free weekend seminar to learn how millionaires buy properties.",
    "Brand new solar panel installation at zero upfront cost! Slash your electric bills to zero with state rebates.",
    "Hot stock alert! This micro-cap lithium mining company is projected to skyrocket 800% next Monday morning. Buy shares now!",
    "Last chance to claim your complementary vacation package to the Bahamas! All luxury resort expenses covered.",
    "Discover how ordinary moms are making $7,500 every single week posting reviews on Google and YouTube from home.",
    "Free trial sample of our top rated weight loss keto gummies. Just cover a tiny $2.95 shipping and handling charge.",
    "Upgrade your kitchen with our top-selling ceramic non-stick cookware set at an unbelievable 70% flash sale discount!",
    "Protect your home and family with a modern smart wireless security alarm system. Free installation and equipment today!"
]

PHISHING_SAMPLES = [
    "URGENT: Your PayPal account has been temporarily restricted due to unauthorized login attempts. Verify your identity immediately at http://paypal-security-check.net/login or your account will be permanently closed.",
    "SECURITY ALERT from Bank of America: Suspicious wire transaction of $2,450.00 detected. If you did not authorize this, click here immediately: http://192.168.1.105/boa-verify to cancel transaction and secure your funds.",
    "Critical Notice: Your Microsoft Office 365 password will expire in 2 hours. Keep your existing password by logging in through our security portal: http://login-microsoftonline-verify.com/auth",
    "Dear Chase Customer, We noticed unusual activity on your debit card ending in 4921. Your card has been suspended. Please confirm your billing address and SSN at http://chase-card-restore.com/verification",
    "URGENT TAX NOTIFICATION: Internal Revenue Service IRS has identified a pending tax refund of $1,420.50 in your name. Submit your direct deposit details and Social Security number at http://irs-gov-refund-portal.org",
    "Netflix Billing Issue: We could not process your monthly payment. Your streaming service will be terminated within 24 hours unless you update your credit card details at http://netflix-billing-update-service.com",
    "DHL Express Delivery: Your parcel #US-89102 could not be delivered due to an incorrect shipping address. Pay $1.95 redelivery fee and update your address at http://dhl-package-reschedule.top/track",
    "Google Account Security Warning: Someone in Moscow, Russia just attempted to access your Google account with your correct password. Secure your account immediately: http://myaccount-google-security-verify.com",
    "Wells Fargo Urgent Alert: Account suspended due to repeated incorrect password entries. Restore full account access now by verifying your banking credentials at http://wellsfargo-access-portal.net/unlock",
    "Your Apple ID has been locked for security reasons. Unauthorized purchases were attempted on iTunes. To unlock your account, confirm your personal information at http://appleid-apple-support-recovery.com",
    "Internal IT Support Helpdesk: We are performing mandatory mailbox migration to modern servers. All employees must authenticate credentials at http://company-webmail-system-login.com to avoid account termination.",
    "Amazon Fraud Prevention: A purchase of iPhone 15 Pro Max for $1,199.00 was ordered using your account. If this was not you, call 1-800-FAKE-NUM or cancel order at http://amazon-dispute-resolution.cc",
    "FedEx Delivery Notification: Your package is on hold at our distribution facility. Confirm your delivery information and postal code within 12 hours: http://fedex-parcel-dispatch.xyz/verify",
    "Urgent DocuSign Document: You have an urgent confidential signature request pending from your HR department. Review and sign document using your corporate email login: http://docusign-secure-document-sign.info",
    "Coinbase Security Notice: A withdrawal request of 1.45 BTC has been initiated. If you did not make this request, freeze your crypto account immediately at http://coinbase-asset-security.net/freeze",
    "Payroll Department Notice: Your direct deposit information could not be verified for this pay period. Update your bank routing and account number at http://payroll-portal-verification.com/update to receive salary.",
    "Facebook / Meta Security Alert: Your business page is scheduled for deletion due to copyright infringement reports. Appeal this decision within 24 hours at http://meta-policy-appeal-support.com",
    "Dropbox Storage Full: Your shared files will be deleted in 48 hours. Validate your corporate user account to maintain cloud storage: http://dropbox-user-storage-upgrade.org/validate",
    "USPS Final Notice: We were unable to deliver your package due to missing apartment number. Click here to confirm address and pay redelivery postage: http://usps-tracking-redelivery.biz/confirm",
    "Action Required: Your LinkedIn account has been flagged for violating community standards. Verify your phone number and identity at http://linkedin-account-safety-check.com/verify or face permanent suspension.",
    "URGENT: Your university student portal credentials must be re-validated for the current academic session. Log in here: http://university-portal-auth.site/login or your course access will be deactivated.",
    "Citibank Alert: New payee added to your mobile banking account. If you did not approve this payee, cancel immediately at http://citibank-fraud-prevention.net/dispute to avoid unauthorized charges.",
    "Instagram Security: Your account is eligible for the verified badge, but you must confirm ownership within 12 hours at http://instagram-verify-badge-apply.com/login or lose eligibility.",
    "Zoom Meeting Security Update: Critical security patch required to attend upcoming scheduled meetings. Download and run update utility from http://zoom-conference-security-patch.top/download",
    "Workday HR Alert: Mandatory benefits enrollment deadline ends today. Please confirm your social security number and dependent data at http://workday-hr-portal-secure.net/enroll"
]

def generate_variations():
    records = []
    
    # Add legitimate templates with variations
    for text in LEGITIMATE_SAMPLES:
        records.append({"text": text, "label": "legitimate"})
        # slight variations
        records.append({"text": f"Subject: Update - {text}", "label": "legitimate"})
        records.append({"text": f"Fwd: {text}", "label": "legitimate"})
        records.append({"text": f"{text} Thanks, best regards.", "label": "legitimate"})
    
    # Add spam templates with variations
    for text in SPAM_SAMPLES:
        records.append({"text": text, "label": "spam"})
        records.append({"text": f"Special Promotion: {text}", "label": "spam"})
        records.append({"text": f"*** ADVERTISEMENT *** {text} Unsubscribe anytime.", "label": "spam"})
        records.append({"text": f"Dear recipient, {text} Don't wait, order now!", "label": "spam"})
        
    # Add phishing templates with variations
    for text in PHISHING_SAMPLES:
        records.append({"text": text, "label": "phishing"})
        records.append({"text": f"URGENT ACTION REQUIRED: {text}", "label": "phishing"})
        records.append({"text": f"Security Alert Notification: {text} Please do not ignore this warning.", "label": "phishing"})
        records.append({"text": f"Dear Valued Customer, {text} Failure to respond will result in account cancellation.", "label": "phishing"})

    # Shuffle dataset
    random.seed(42)
    random.shuffle(records)
    
    df = pd.DataFrame(records)
    return df

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    df = generate_variations()
    output_path = os.path.join("data", "emails.csv")
    df.to_csv(output_path, index=False)
    print(f"Dataset successfully generated at {output_path}")
    print(f"Total samples: {len(df)}")
    print("Class distribution:")
    print(df["label"].value_counts())
