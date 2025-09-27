"""
Mock Telecoms Ticket Data Generator

Generates realistic customer service tickets for a South African telecommunications company.
Supports multiple categories: BILLING, TECHNICAL, SALES, COMPLAINTS, NETWORK, ACCOUNT.
"""

import random
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta
from typing import List, Dict, Tuple


class TelecomsTicketGenerator:
    """Generates mock telecoms customer service tickets with realistic South African context."""
    
    def __init__(self, seed: int = 42) -> None:
        """Initialize the generator with South African locale and predefined categories."""
        random.seed(seed)
        self.fake = Faker(['en_US', 'en_GB'])  # US + British English (en_ZA not available)
        Faker.seed(seed)
        
        # Target distribution based on typical call center volumes
        self.categories = {
            'BILLING': 1200,     # Most common - billing disputes
            'TECHNICAL': 1000,   # Second most - connection issues  
            'SALES': 800,        # Sales inquiries and upgrades
            'COMPLAINTS': 700,   # Service complaints
            'NETWORK': 600,      # Infrastructure issues
            'ACCOUNT': 700       # Account management
        }
        
        # South African specific context
        self.sa_locations = [
            'Johannesburg', 'Cape Town', 'Durban', 'Pretoria', 'Port Elizabeth',
            'Bloemfontein', 'East London', 'Polokwane', 'Nelspruit', 'Kimberley',
            'Rustenburg', 'George', 'Witbank', 'Vanderbijlpark', 'Centurion',
            'Randburg', 'Roodepoort', 'Boksburg', 'Benoni', 'Kempton Park'
        ]
        
        self.currency = "R"  # South African Rand
        
    def generate_dataset(self) -> pd.DataFrame:
        """Generate complete dataset with quality validation."""
        print("🚀 Starting telecoms ticket generation...")
        
        all_tickets = []
        
        for category, count in self.categories.items():
            print(f"📝 Generating {count} {category} tickets...")
            category_tickets = self._generate_category_tickets(category, count)
            all_tickets.extend(category_tickets)
        
        # Create DataFrame and validate
        df = pd.DataFrame(all_tickets)
        validated_df = self._validate_and_clean_data(df)
        
        print(f"✅ Generated {len(validated_df)} total tickets")
        print(f"📊 Category distribution: {validated_df['category'].value_counts().to_dict()}")
        
        return validated_df
    
    def _generate_category_tickets(self, category: str, count: int) -> List[Dict]:
        """Generate tickets for a specific category with realistic scenarios."""
        tickets = []
        
        for i in range(count):
            ticket = self._generate_base_ticket(category, i)
            ticket['ticket_text'] = self._generate_category_text(category)
            tickets.append(ticket)
            
        return tickets
    
    def _generate_base_ticket(self, category: str, index: int) -> Dict:
        """Generate base ticket metadata."""
        # Generate realistic timestamp (last 30 days)
        created_date = self.fake.date_time_between(start_date='-30d', end_date='now')
        
        # Priority distribution: 60% MEDIUM, 25% HIGH, 15% LOW
        priority = random.choices(['LOW', 'MEDIUM', 'HIGH'], weights=[15, 60, 25])[0]
        
        # Customer type: 70% residential, 30% business
        customer_type = random.choices(['residential', 'business'], weights=[70, 30])[0]
        
        return {
            'ticket_id': f'TCK{str(index + 1).zfill(5)}_{category}',
            'category': category,
            'priority': priority,
            'created_date': created_date,
            'customer_type': customer_type,
            'location': random.choice(self.sa_locations)
        }
    
    def _generate_category_text(self, category: str) -> str:
        """Generate realistic ticket text for each category."""
        
        if category == 'BILLING':
            return self._generate_billing_text()
        elif category == 'TECHNICAL':
            return self._generate_technical_text()
        elif category == 'SALES':
            return self._generate_sales_text()
        elif category == 'COMPLAINTS':
            return self._generate_complaints_text()
        elif category == 'NETWORK':
            return self._generate_network_text()
        elif category == 'ACCOUNT':
            return self._generate_account_text()
        else:
            return "General inquiry about telecoms services."
    
    def _generate_billing_text(self) -> str:
        """Generate realistic billing-related ticket text."""
        templates = [
            f"My bill this month is {self.currency}{random.randint(200, 1000)} higher than usual but I haven't changed my plan. Can you please explain the extra charges?",
            f"I was charged {self.currency}{random.randint(50, 300)} for international calls but I never made any calls overseas. This must be an error.",
            f"My debit order failed but the money of {self.currency}{random.randint(500, 1500)} was still deducted from my account. Please reverse this duplicate charge.",
            f"Why am I paying for premium sports channels when I cancelled them {random.randint(2, 6)} months ago?",
            f"I received a bill for {self.currency}{random.randint(1000, 3000)} but my normal monthly cost is {self.currency}{random.randint(500, 800)}. This can't be correct.",
            f"There are data charges of {self.currency}{random.randint(100, 500)} on my bill but I have unlimited data. Please investigate.",
            f"I'm being charged for roaming fees of {self.currency}{random.randint(200, 800)} but I haven't left {random.choice(self.sa_locations)} this month.",
            f"My contract says {self.currency}{random.randint(400, 900)} per month but you've been charging me {self.currency}{random.randint(600, 1200)}. Fix this please.",
        ]
        
        return self._add_text_variations(random.choice(templates))
    
    def _generate_technical_text(self) -> str:
        """Generate realistic technical support ticket text."""
        templates = [
            f"My internet speed is only {random.randint(5, 30)}Mbps but I'm paying for {random.randint(50, 200)}Mbps. This has been going on for {random.randint(3, 14)} days.",
            f"I keep losing connection every {random.randint(30, 180)} minutes and have to restart my router. Very frustrating when working from home.",
            f"My landline has terrible static noise and I can barely hear callers. This started {random.randint(2, 10)} days ago.",
            f"WiFi signal is very weak in my {random.choice(['bedroom', 'kitchen', 'study', 'lounge'])}. Can't stream videos or video call.",
            f"The internet goes down completely around {random.randint(6, 10)}PM every evening for about {random.randint(30, 120)} minutes.",
            f"My email isn't working properly, can't send or receive messages since {random.randint(1, 5)} days ago.",
            f"Call quality is terrible, everyone sounds like they're underwater. This is affecting my business calls.",
            f"Internet works fine during the day but becomes unusable after {random.randint(6, 9)}PM when everyone gets home.",
        ]
        
        return self._add_text_variations(random.choice(templates))
    
    def _generate_sales_text(self) -> str:
        """Generate realistic sales inquiry ticket text."""
        templates = [
            f"I want to upgrade to fiber, what packages do you have available in {random.choice(self.sa_locations)}?",
            f"Can I add more data to my mobile plan without extending my contract? I need about {random.randint(20, 100)}GB more per month.",
            f"What's the difference between your {random.randint(50, 100)}Mbps and {random.randint(100, 200)}Mbps fiber packages?",
            f"I'm moving to {random.choice(self.sa_locations)} next month, can you help me transfer all my services?",
            f"Do you have any special deals for new customers? My neighbor got fiber for {self.currency}{random.randint(400, 800)} per month.",
            f"I want to bundle my mobile, internet and TV services. What discount can you offer?",
            f"My contract expires in {random.randint(1, 6)} months, what upgrade options do I have?",
            f"Can I get a second internet line installed for my home office? What would that cost?",
        ]
        
        return self._add_text_variations(random.choice(templates))
    
    def _generate_complaints_text(self) -> str:
        """Generate realistic complaint ticket text."""
        templates = [
            f"This is the {random.choice(['second', 'third', 'fourth'])} time this month my service has been down. I'm paying for reliable internet!",
            f"Your technician was supposed to come {random.randint(2, 7)} days ago and never showed up. Didn't even call to cancel.",
            f"I've been on hold for {random.randint(30, 90)} minutes trying to speak to someone. This is completely unacceptable service.",
            f"You promised to fix my connection issue a week ago and still nothing has been done. I'm losing money working from home.",
            f"The customer service rep was extremely rude when I called about my billing issue. This is not how you treat paying customers.",
            f"I've called {random.randint(3, 8)} times about the same problem and each person tells me something different. Sort this out!",
            f"Your installation team damaged my garden and didn't even apologize. Then they left without finishing the job properly.",
            f"I'm cancelling my contract because your service is terrible. I want a manager to call me immediately.",
        ]
        
        return self._add_text_variations(random.choice(templates))
    
    def _generate_network_text(self) -> str:
        """Generate realistic network/infrastructure ticket text."""
        templates = [
            f"There's a complete internet outage in our area - {random.choice(self.sa_locations)} {random.choice(['North', 'South', 'East', 'West', 'Central'])}. Nobody has service.",
            f"Multiple people in our street have no signal since yesterday morning. Is there a tower problem?",
            f"The cell tower near us seems to be malfunctioning. Signal strength dropped from 4 bars to 1 bar.",
            f"Fiber cables in our complex were damaged during construction work. When will this be fixed?",
            f"There's been no mobile coverage in {random.choice(self.sa_locations)} CBD since {random.randint(6, 48)} hours ago.",
            f"The whole suburb has slow internet today. Is there network maintenance happening?",
            f"Power outage affected the local exchange, when will internet service be restored?",
            f"Underground cables were cut during road works on {self.fake.street_name()} street. Multiple houses affected.",
        ]
        
        return self._add_text_variations(random.choice(templates))
    
    def _generate_account_text(self) -> str:
        """Generate realistic account management ticket text."""
        templates = [
            f"I need to update my email address from {self.fake.email()} to {self.fake.email()} on my account.",
            f"Can you help me reset my online account password? I can't remember what I changed it to.",
            f"I want to add my {random.choice(['spouse', 'partner', 'son', 'daughter'])} as an authorized user on my account.",
            f"I'm moving to {random.choice(self.sa_locations)} next month, please update my billing and service address.",
            f"How do I change from paper bills to email statements? Want to go paperless.",
            f"I need to update my ID number on the account, I made a mistake during registration.",
            f"Can I get a copy of my last {random.randint(3, 12)} months' bills sent to my email?",
            f"My credit card expires next month, how do I update my payment method for the debit order?",
        ]
        
        return self._add_text_variations(random.choice(templates))
    
    def _add_text_variations(self, text: str) -> str:
        """Add realistic variations to make text more natural."""
        # Add occasional typos and informal language
        variations = [
            text,  # Keep original
            text.replace("My ", "my "),  # Lowercase start sometimes
            text.replace("Can you", "could you"),  # Politeness variation
            text.replace("I want", "I'd like"),  # Formal variation
            text + " Thanks.",  # Add politeness
            text + " Please help ASAP.",  # Add urgency
        ]
        
        # Occasionally add some typos for realism
        if random.random() < 0.1:  # 10% chance of minor typo
            text = text.replace("the", "teh") if "the" in text else text
        
        return random.choice(variations)
    
    def _validate_and_clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Comprehensive data quality validation and cleaning."""
        print("🔍 Running data quality checks...")
        
        # Remove any duplicates
        initial_count = len(df)
        df = df.drop_duplicates(subset=['ticket_text'])
        if len(df) < initial_count:
            print(f"⚠️  Removed {initial_count - len(df)} duplicate tickets")
        
        # Validate text length (10-500 characters)
        df = df[df['ticket_text'].str.len().between(10, 500)]
        
        # Remove any null values
        df = df.dropna()
        
        # Validate categories
        valid_categories = set(self.categories.keys())
        df = df[df['category'].isin(valid_categories)]
        
        # Shuffle the dataset
        df = df.sample(frac=1).reset_index(drop=True)
        
        # Validate final dataset quality
        quality_report = self._generate_quality_report(df)
        print("📋 Data Quality Report:")
        for check, result in quality_report.items():
            status = "✅" if result else "❌"
            print(f"   {status} {check}")
            
        return df
    
    def _generate_quality_report(self, df: pd.DataFrame) -> Dict[str, bool]:
        """Generate comprehensive data quality report."""
        return {
            'sufficient_volume': len(df) >= 5000,
            'category_balance': all(count >= 500 for count in df['category'].value_counts()),
            'no_duplicates': len(df) == len(df.drop_duplicates(subset=['ticket_text'])),
            'text_length_valid': df['ticket_text'].str.len().between(10, 500).all(),
            'no_missing_values': df.isnull().sum().sum() == 0,
            'category_coverage': set(df['category']) == set(self.categories.keys()),
            'realistic_timestamps': df['created_date'].min() >= (datetime.now() - timedelta(days=35)),
            'priority_distribution': len(df['priority'].unique()) == 3
        }
    
    def create_train_test_splits(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Create stratified train/validation/test splits."""
        from sklearn.model_selection import train_test_split
        
        # First split: train (70%) and temp (30%)
        train_df, temp_df = train_test_split(
            df, 
            test_size=0.3, 
            stratify=df['category'], 
            random_state=42
        )
        
        # Second split: validation (15%) and test (15%)
        val_df, test_df = train_test_split(
            temp_df, 
            test_size=0.5, 
            stratify=temp_df['category'], 
            random_state=42
        )
        
        print(f"📊 Data splits created:")
        print(f"   Training: {len(train_df)} samples ({len(train_df)/len(df)*100:.1f}%)")
        print(f"   Validation: {len(val_df)} samples ({len(val_df)/len(df)*100:.1f}%)")
        print(f"   Test: {len(test_df)} samples ({len(test_df)/len(df)*100:.1f}%)")
        
        return train_df, val_df, test_df


def main():
    """Generate the complete telecoms dataset."""
    generator = TelecomsTicketGenerator()
    
    # Generate full dataset
    dataset = generator.generate_dataset()
    
    # Create train/val/test splits
    train_df, val_df, test_df = generator.create_train_test_splits(dataset)
    
    # Save datasets
    dataset.to_csv('data/telecoms_tickets_full.csv', index=False)
    train_df.to_csv('data/telecoms_tickets_train.csv', index=False)
    val_df.to_csv('data/telecoms_tickets_val.csv', index=False)  
    test_df.to_csv('data/telecoms_tickets_test.csv', index=False)
    
    print("🎉 Dataset generation complete!")
    print("📁 Files saved:")
    print("   - data/telecoms_tickets_full.csv")
    print("   - data/telecoms_tickets_train.csv")
    print("   - data/telecoms_tickets_val.csv")
    print("   - data/telecoms_tickets_test.csv")


if __name__ == "__main__":
    main()