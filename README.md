# Meetup Attendee Export Manager

This project helps to manage and match attendee data exported from the Meetup platform. It is designed to solve the issue of mismatched data between two different types of exports: one providing detailed attendee information without RSVP status, and another with RSVP status but limited user data. This tool aims to streamline the process of matching these exports and reduce the manual effort required.

## Problem

Meetup allows you to export event attendee data, but there are two types of exports with different limitations:

1. **Registration responses (No RSVP Status)**:

   - Contains proNetwork's questions like first name, last name, and organization.
   - Includes all attendees, including those on the waitlist and those who RSVPed "No", but **doesn't specify the RSVP status**.

   Example fields:

   ```
   "updatedAt", "chapter.name", "event.title", "First name", "Last name", "Organization name", "Main reason for attending"
   ```

2. **Attendee Details (With RSVP Status)**:

   - Includes attendee RSVP status, but the data is limited to user IDs and profile information.

   Example fields:

   ```
   "Name", "User ID", "RSVP", "Guests", "RSVPed on", "Any dietary requirements?"
   ```

### The Problem:

There is **no user ID match** between these two exports, making it difficult to match attendees who RSVPed "Yes" with their detailed information, especially when printing badges. This project solves this by helping to match the data from both exports automatically.

## Features

- Fetch attendee data from the Meetup API using GraphQL.
- Match data between the two types of exports.
- Store the matched data in csv file
-

## Installation

This project uses PDM (Python Development Master) for Python package management.

### Prerequisites

- Python 3.12 or higher
- PDM for managing dependencies

### Setup

1. **Clone the repository:**

   ```bash
   git clone git@github.com:estyxx/meetup-export.git
   cd meetup-export
   ```

2. **Install dependencies:**

   ```bash
   pdm install
   ```

3. **Set Up a Meetup Developer Account:**

   - Go to the [Meetup Developer Portal](https://secure.meetup.com/meetup_api/) and create an OAuth client.
   - You will get a **Client Key**, **Client Secret**, and **Signing Key ID**.

4. **Configure Environment Variables:**

   Copy the `.env.copy` file to `.env` and modify it with your own values:

   ```plaintext
   MEETUP_COM_CLIENT_KEY=your_client_key_here
   MEETUP_COM_SECRET=your_secret_here
   MEETUP_COM_SIGNING_KEY_ID=your_signing_key_id_here
   MEETUP_COM_AUTHORIZED_MEMBER_ID=your_authorized_member_id_here
   MEETUP_COM_PRIVATE_KEY_PATH=path_to_your_private_key.pem
   ```

   The private key is used for JWT authentication.

## Usage

You can use PDM scripts to run the project components:

### Execute the main script

This script processes the exports and matches the attendee data:

```bash
pdm run export
```

## Output

The script will generate the following files in the `outputs` directory:

- `merged_attendees.csv`: An Excel file with attendee details matched to their RSVP status.

## How It Works

1. **Fetch Data from Meetup**: The project uses the Meetup API and GraphQL to fetch event attendee information.
2. **Match Data**: The script processes the two types of exports and matches attendees based on name and other available information.
3. **Save Data**: The matched data is saved in both Excel and JSON formats.

## Limitations

- **Matching Accuracy**: Matching attendees based on name may not be perfect, especially if there are duplicate names or incomplete data.

- **Permissions**: Accessing certain data via the Meetup API (like Pro Network questions) requires special permissions, which may not always be available.
