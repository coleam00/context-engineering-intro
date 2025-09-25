## FEATURE:

Build **NaruNotes**, a native iOS app in Swift using SwiftUI and CoreData. NaruNotes allows parents to curate and send intentional, emotionally resonant family updates via digital (email) or physical (mail) newsletters.

The app includes the following **core modules**:

### 1. Recipient Management
- Add, edit, delete recipients.
- Each recipient can be tagged as digital (email) or print (mail), with validations for each (e.g. email required for digital).
- All data is stored locally using CoreData for now.
- Fields include: first name, last name, email, mailing address, recipient type toggles (email/print), notes (optional).

### 2. Photo & Caption Upload
- Select photos from the device library.
- Attach optional captions per photo.
- Support photo reordering within a newsletter.
- Photos must be saved in high-quality format, optimized for large-screen email viewing and future-proofed for print.

### 3. Newsletter Composition
- Combine photos + text blocks into a flexible layout using predefined templates.
- Users can choose a layout style (e.g. photo-first, text-first, seasonal themes).
- Support draft saving, previewing, and editing before sending.

### 4. Template System
- Implement a modular template system starting with 2–3 built-in layouts.
- Templates define layout rules for how photos and text are displayed.
- Define templates using Swift structs or JSON if needed, with future extensibility in mind (e.g. holiday themes, designer-created templates).

### 5. Sending & Delivery
- Users can select recipients from their address book.
- If recipient is tagged for email, generate an HTML-formatted newsletter and send it using a future email delivery API (e.g., Postmark or Mailgun).
- If recipient is tagged for print, mark the newsletter for future export (PDF support can be stubbed).
- Email delivery backend can be stubbed/instrumented for now – integration comes later.

### 6. User Authentication
- Authenticate users via Google Sign-In using OAuth SDK or Firebase.
- Associate newsletter content with a single user account (multi-user functionality not required in MVP).

### 7. Dashboard & Archive
- Display current draft in progress and past sent newsletters.
- Allow duplication of previous newsletters for quick editing and reuse.
- Archive view should show thumbnails, titles, and send dates.

### 8. Local-First Architecture (MVP)
- All content is stored locally using CoreData and local file storage.
- Stub integration points for future cloud sync and email dispatch.

## DOCUMENTATION:

- SwiftUI: https://developer.apple.com/documentation/swiftui/
- CoreData: https://developer.apple.com/documentation/coredata/
- Google Sign-In (iOS): https://developers.google.com/identity/sign-in/ios
- PhotoKit: https://developer.apple.com/documentation/photokit/
- Swift Package Manager: https://developer.apple.com/documentation/swift_packages/

## OTHER CONSIDERATIONS:

- Photos must remain high resolution, especially for email recipients who will read newsletters on large displays.
- The app should use UUIDs for recipients, photos, and newsletters to prepare for future syncing and backend extensions.
- Show inline warnings if a recipient is selected for print but has no valid mailing address.
- Use a modular SwiftUI architecture with separation of concerns per feature (e.g. forms, lists, detail views).
- Use MVVM-lite architecture where helpful, but do not over-engineer.
- Include an `.env.example` only if any API keys (e.g., for Gmail, future email integration) are introduced.
- Avoid third-party backend services in MVP. No Firebase, Supabase, or remote databases unless needed for authentication.
- Project must be scoped to stay within a $3K MVP budget and part-time dev capacity – build the essentials first and leave hooks for future expansion.
