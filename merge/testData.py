
xml0 = '''
<ItpDocumentRequest xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <DocumentCode>AgreementTimerExtended</DocumentCode>
    <UrlLinks list="true">
        <ItpUrlLink>
            <LinkType>AppUrl</LinkType>
            <LinkUrl>http://TrisHibLet.Test1Lettings.Property-Portal.uk:81/</LinkUrl>
        </ItpUrlLink>
        <ItpUrlLink>
            <LinkType>ImageStore</LinkType>
            <LinkUrl>http://Images.TestLettings.Property-Portal.uk/</LinkUrl>
        </ItpUrlLink>
    </UrlLinks>
    <AppUrl>http://TrisHibLet.Test1Lettings.Property-Portal.uk:81/</AppUrl>
    <EMailUser>
        <UserId>1f33ded2-c07d-45a5-be6a-08328194f0f5</UserId>
        <Title>Dr</Title>
        <FirstName>Harold</FirstName>
        <LastName>Chrysler</LastName>
        <Email>trishiblet@9yds-testing.co.uk</Email>
        <HomeTel>474581889</HomeTel>
        <WorkTel>1042066969</WorkTel>
        <Mobile>200680493</Mobile>
        <PropertyUserType>
            <Value>ManuallyInvitedTenant</Value>
            <Description>Tenant</Description>
            <Id>4</Id>
        </PropertyUserType>
        <Addresses list="true">
            <ItpAddress>
                <AddressId>5f547622-ded3-e511-81e6-06ab496445e9</AddressId>
                <AddressLine1>18, Top Gear Lane</AddressLine1>
                <City>Test Town</City>
                <Postcode>X9 9LF</Postcode>
                <CurrentAddress>true</CurrentAddress>
                <ResidencyStatus>PrivateRented</ResidencyStatus>
                <ResidencyStatusDesc>Private Rented</ResidencyStatusDesc>
            </ItpAddress>
        </Addresses>
        <IdCheckStatus>
            <Value>Passed</Value>
            <Description>ID matched and ID Check Passed</Description>
            <Id>1</Id>
        </IdCheckStatus>
        <NextOfKin>
            <Name>Ted Accountant</Name>
            <TelephoneNumber>01234 567891</TelephoneNumber>
            <Email>test@test.com</Email>
            <ContactAddress>
                <AddressId>babca730-ded3-e511-81e6-06ab496445e9</AddressId>
                <AddressLine1>UserAddress 1</AddressLine1>
                <AddressLine2>UserAddress 2</AddressLine2>
                <City>City</City>
                <County>County</County>
                <Postcode>PO5 8DE</Postcode>
                <Country>Country</Country>
                <CurrentAddress>true</CurrentAddress>
                <ResidencyStatus>NotSet</ResidencyStatus>
                <ResidencyStatusDesc>Unknown</ResidencyStatusDesc>
            </ContactAddress>
        </NextOfKin>
        <UserDocuments list="true">
            <ItpDocument>
                <Url>https://project-equalet-documents.s3.amazonaws.com/Test1/1f33ded2-c07d-45a5-be6a-08328194f0f5/Documents/CreditReport-21MountainRoad-20160215121822404.html</Url>
                <DocumentType>CreditCheckReport</DocumentType>
                <DocumentReference>CreditReport-21 Mountain Road-20160215121822404.html</DocumentReference>
                <DocumentDate>2016-02-15T12:18:22.45</DocumentDate>
                <StartDate xsi:nil="true"/>
                <EndDate xsi:nil="true"/>
                <Verified>true</Verified>
            </ItpDocument>
            <ItpDocument>
                <Url>https://project-equalet-documents.s3.amazonaws.com/Test1/1f33ded2-c07d-45a5-be6a-08328194f0f5/Documents/IdCheckReport-0.html</Url>
                <DocumentType>IdCheckReport</DocumentType>
                <DocumentReference>IdCheckReport-0.html</DocumentReference>
                <DocumentDate>2016-02-15T12:17:56.763</DocumentDate>
                <StartDate xsi:nil="true"/>
                <EndDate xsi:nil="true"/>
                <Verified>true</Verified>
            </ItpDocument>
            <ItpDocument>
                <Url>https://project-equalet-documents.s3.amazonaws.com/Test1/1f33ded2-c07d-45a5-be6a-08328194f0f5/Documents/20160215121832747.pdf</Url>
                <DocumentType>ProofOfResidence</DocumentType>
                <DocumentReference>ref-ProofOfResidence</DocumentReference>
                <DocumentDate xsi:nil="true"/>
                <StartDate>2015-02-15T12:18:21.987</StartDate>
                <EndDate>2017-02-15T12:18:21.987</EndDate>
                <Verified>true</Verified>
            </ItpDocument>
            <ItpDocument>
                <Url>https://project-equalet-documents.s3.amazonaws.com/Test1/1f33ded2-c07d-45a5-be6a-08328194f0f5/Documents/20160215121832950.pdf</Url>
                <DocumentType>PhotoId</DocumentType>
                <DocumentReference>ref-PhotoId</DocumentReference>
                <DocumentDate xsi:nil="true"/>
                <StartDate>2015-02-15T12:18:22.207</StartDate>
                <EndDate>2017-02-15T12:18:22.207</EndDate>
                <Verified>true</Verified>
            </ItpDocument>
            <ItpDocument>
                <Url>https://project-equalet-documents.s3.amazonaws.com/Test1/1f33ded2-c07d-45a5-be6a-08328194f0f5/Documents/20160215121833700.pdf</Url>
                <DocumentType>ImmigrationStatusDoc</DocumentType>
                <DocumentReference>ref-ImmigrationStatusDoc</DocumentReference>
                <DocumentDate xsi:nil="true"/>
                <StartDate>2015-02-15T12:18:22.963</StartDate>
                <EndDate>2017-02-15T12:18:22.963</EndDate>
                <Verified>true</Verified>
            </ItpDocument>
        </UserDocuments>
        <ControllingOrganisation>
            <OrganisationStatus>Limited</OrganisationStatus>
            <OrganisationType>Advertising</OrganisationType>
            <RegisteredOrganisationName>TrisHibLet Ltd</RegisteredOrganisationName>
            <TradingName>TrisHibLet</TradingName>
            <LogoUrl>http://images.TestLettings.Property-Portal.uk/b2b/hiblenlets.gif</LogoUrl>
            <RegistrationNumber>11111111</RegistrationNumber>
            <VatNumber>928289676x</VatNumber>
            <CompanyTelephone>0333 006 3000x</CompanyTelephone>
            <CompanyEmail>theteam@TrisHibLet.co.uk</CompanyEmail>
            <Established>2015-10-01T00:00:00</Established>
            <GrossProfit>0.00</GrossProfit>
            <MarketingType>
                <Value>NoMarketing</Value>
                <Description>NoMarketing</Description>
                <Id>2</Id>
            </MarketingType>
            <ShowCoBranding>true</ShowCoBranding>
            <OrganisationUsers list="true">
                <ItpOrganisationUser>
                    <OrganisationUserType>
                        <Value>OrganisationAdministrator</Value>
                        <Description>Organisation Administrator</Description>
                        <Id>1</Id>
                    </OrganisationUserType>
                    <OrganisationUserRole>
                        <Value>Owner</Value>
                        <Description>Owner</Description>
                        <Id>1</Id>
                    </OrganisationUserRole>
                    <SigningAuthority>true</SigningAuthority>
                    <Contact>
                        <Name>Harold Chrysler</Name>
                        <TelephoneNumber>200680493</TelephoneNumber>
                        <Email>trishiblet@9yds-testing.co.uk</Email>
                        <ContactAddress>
                            <AddressId>5f547622-ded3-e511-81e6-06ab496445e9</AddressId>
                            <AddressLine1>18, Top Gear Lane</AddressLine1>
                            <City>Test Town</City>
                            <Postcode>X9 9LF</Postcode>
                            <CurrentAddress>true</CurrentAddress>
                            <ResidencyStatus>PrivateRented</ResidencyStatus>
                            <ResidencyStatusDesc>Private Rented</ResidencyStatusDesc>
                        </ContactAddress>
                    </Contact>
                </ItpOrganisationUser>
                <ItpOrganisationUser>
                    <OrganisationUserType>
                        <Value>OrganisationAdministrator</Value>
                        <Description>Organisation Administrator</Description>
                        <Id>1</Id>
                    </OrganisationUserType>
                    <OrganisationUserRole>
                        <Value>Owner</Value>
                        <Description>Owner</Description>
                        <Id>1</Id>
                    </OrganisationUserRole>
                    <SigningAuthority>true</SigningAuthority>
                    <Contact>
                        <Name>Org Admin</Name>
                        <Email>TrisHibLet@hiblen.com</Email>
                    </Contact>
                </ItpOrganisationUser>
            </OrganisationUsers>
            <Addresses list="true">
                <ItpAddress>
                    <AddressId>7f5d7904-68d1-e511-81e5-06ab496445e9</AddressId>
                    <AddressLine1>TrisHibLet</AddressLine1>
                    <AddressLine2>PO box 666</AddressLine2>
                    <City>London</City>
                    <Postcode>SW12 9KL</Postcode>
                    <CurrentAddress>true</CurrentAddress>
                    <ResidencyStatus>Owned</ResidencyStatus>
                    <AddressType>
                        <Value>RegisteredOffice</Value>
                        <Description>RegisteredOffice</Description>
                        <Id>2</Id>
                    </AddressType>
                    <ResidencyStatusDesc>Owned</ResidencyStatusDesc>
                </ItpAddress>
                <ItpAddress>
                    <AddressId>805d7904-68d1-e511-81e5-06ab496445e9</AddressId>
                    <AddressLine1>TrisHibLet</AddressLine1>
                    <AddressLine2>PO box 666</AddressLine2>
                    <City>London</City>
                    <Postcode>SW12 9KL</Postcode>
                    <CurrentAddress>true</CurrentAddress>
                    <ResidencyStatus>Owned</ResidencyStatus>
                    <AddressType>
                        <Value>AccountantAddress</Value>
                        <Description>AccountantAddress</Description>
                        <Id>4</Id>
                    </AddressType>
                    <ResidencyStatusDesc>Owned</ResidencyStatusDesc>
                </ItpAddress>
            </Addresses>
            <BankAccounts list="true">
                <ItpBank/>
            </BankAccounts>
        </ControllingOrganisation>
        <LandlordType>
            <Value>NotSet</Value>
            <Description>NotSet</Description>
            <Id>0</Id>
        </LandlordType>
        <ReferencingPaid>true</ReferencingPaid>
        <ReferenceCheckStatus>Passed</ReferenceCheckStatus>
        <ReferenceCheckSoftPass>false</ReferenceCheckSoftPass>
        <GuarantorRequired xsi:nil="true"/>
        <GuarantorAdded>false</GuarantorAdded>
        <AgreementSigningStatus>NotSet</AgreementSigningStatus>
        <ConfirmedUser>true</ConfirmedUser>
        <SigningUser>true</SigningUser>
        <AgencyStaff>true</AgencyStaff>
        <NoPasswordEnteredOnRegistration>false</NoPasswordEnteredOnRegistration>
        <TenantWantsDetails>false</TenantWantsDetails>
        <TenantWantsViewing>false</TenantWantsViewing>
        <IsSmoker>false</IsSmoker>
        <HasPets>true</HasPets>
        <HasDependents>true</HasDependents>
        <IsRegisteringDeposit>false</IsRegisteringDeposit>
    </EMailUser>
    <Property>
        <PropertyId>c0476ede-ddd3-e511-81e6-06ab496445e9</PropertyId>
        <HeatingTypes list="true">
            <ItemOfHeatingType>
                <Value>Gas</Value>
                <Description>Gas</Description>
                <Id>1</Id>
            </ItemOfHeatingType>
            <ItemOfHeatingType>
                <Value>Oil</Value>
                <Description>Oil</Description>
                <Id>4</Id>
            </ItemOfHeatingType>
        </HeatingTypes>
        <Postcode>UB3 4RB</Postcode>
        <Description>Description</Description>
        <PropertyTypeId>
            <Value>House</Value>
            <Description>House</Description>
            <Id>1</Id>
        </PropertyTypeId>
        <PropertyStyleId>
            <Value>Detached</Value>
            <Description>Detached</Description>
            <Id>1</Id>
        </PropertyStyleId>
        <DateAvailable>2016-03-15T00:00:00</DateAvailable>
        <FurnishedId>
            <Value>Partfurnished</Value>
            <Description>Part Furnished</Description>
            <Id>2</Id>
        </FurnishedId>
        <ParkingTypes list="true">
            <ItemOfParkingType>
                <Value>AllocatedParking</Value>
                <Description>Allocated Parking</Description>
                <Id>2</Id>
            </ItemOfParkingType>
            <ItemOfParkingType>
                <Value>Garage</Value>
                <Description>Garage</Description>
                <Id>8</Id>
            </ItemOfParkingType>
        </ParkingTypes>
        <OutsideSpaces list="true">
            <ItemOfOutsideSpaceType>
                <Value>CommunalGarden</Value>
                <Description>Communal Garden</Description>
                <Id>1</Id>
            </ItemOfOutsideSpaceType>
            <ItemOfOutsideSpaceType>
                <Value>FrontGarden</Value>
                <Description>Front Garden</Description>
                <Id>4</Id>
            </ItemOfOutsideSpaceType>
        </OutsideSpaces>
        <StudentsAllowed>true</StudentsAllowed>
        <ContractMonths>60</ContractMonths>
        <TenureId>
            <Value>Freehold</Value>
            <Description>Freehold</Description>
            <Id>1</Id>
        </TenureId>
        <AddressLine1>21 Mountain Road</AddressLine1>
        <City>Hayes</City>
        <County>Middlesex</County>
        <Country>UK</Country>
        <GasSupplied>true</GasSupplied>
        <Balcony>false</Balcony>
        <HasBuildingsInsurance>false</HasBuildingsInsurance>
        <HasContentsInsurance>false</HasContentsInsurance>
        <PropertyImages list="true">
            <ItpPropertyImage>
                <Url>https://project-equalet-documents.s3.amazonaws.com/Test1/c0476ede-ddd3-e511-81e6-06ab496445e9/Photos/20160215121559173.jpg</Url>
            </ItpPropertyImage>
        </PropertyImages>
        <PropertyDocuments list="true">
            <ItpDocument>
                <Url>https://project-equalet-documents.s3.amazonaws.com/Test1/c0476ede-ddd3-e511-81e6-06ab496445e9/Documents/20160215121808482.pdf</Url>
                <DocumentType>Epc</DocumentType>
                <DocumentReference>ref-Epc</DocumentReference>
                <DocumentDate xsi:nil="true"/>
                <StartDate>2015-02-15T12:17:57.74</StartDate>
                <EndDate>2017-02-15T12:17:57.74</EndDate>
                <Verified>true</Verified>
            </ItpDocument>
            <ItpDocument>
                <Url>https://project-equalet-documents.s3.amazonaws.com/Test1/c0476ede-ddd3-e511-81e6-06ab496445e9/Documents/20160215121808795.pdf</Url>
                <DocumentType>GasSafety</DocumentType>
                <DocumentReference>ref-GasSafety</DocumentReference>
                <DocumentDate xsi:nil="true"/>
                <StartDate>2015-02-15T12:17:58.047</StartDate>
                <EndDate>2017-02-15T12:17:58.047</EndDate>
                <Verified>true</Verified>
            </ItpDocument>
            <ItpDocument>
                <Url>https://project-equalet-documents.s3.amazonaws.com/Test1/c0476ede-ddd3-e511-81e6-06ab496445e9/Documents/20160215121809670.pdf</Url>
                <DocumentType>ProofOfOwnership</DocumentType>
                <DocumentReference>ref-ProofOfOwnership</DocumentReference>
                <DocumentDate xsi:nil="true"/>
                <StartDate>2015-02-15T12:17:58.923</StartDate>
                <EndDate>2017-02-15T12:17:58.923</EndDate>
                <Verified>true</Verified>
            </ItpDocument>
        </PropertyDocuments>
        <PropertyRooms list="true">
            <ItpPropertyRoom>
                <RoomTypeId>
                    <Value>Kitchen</Value>
                    <Description>Kitchen</Description>
                    <Id>7</Id>
                </RoomTypeId>
                <Quantity>1</Quantity>
                <Name>Kitchen</Name>
            </ItpPropertyRoom>
            <ItpPropertyRoom>
                <RoomTypeId>
                    <Value>Bedroom</Value>
                    <Description>Bedroom</Description>
                    <Id>1</Id>
                </RoomTypeId>
                <Quantity>3</Quantity>
                <Name>Bedroom</Name>
            </ItpPropertyRoom>
            <ItpPropertyRoom>
                <RoomTypeId>
                    <Value>Cloakroom</Value>
                    <Description>Cloakroom</Description>
                    <Id>4</Id>
                </RoomTypeId>
                <Quantity>2</Quantity>
                <Name>Cloakroom</Name>
            </ItpPropertyRoom>
        </PropertyRooms>
        <PropertyAdverts list="true">
            <ItpPropertyAdvert>
                <ProviderType>
                    <Value>Rightmove</Value>
                    <Description>Rightmove</Description>
                    <Id>1</Id>
                </ProviderType>
                <AdvertUrl>http://www.adftest.rightmove.com/property-to-rent/property-56842607.html</AdvertUrl>
                <AgentRef>1f5c2822-5284-445d-80ef-cee4d555900d__Test1__</AgentRef>
                <AdvertListingStatus>LetAgreed</AdvertListingStatus>
                <FirstListedDate>2016-02-15T12:16:58</FirstListedDate>
                <TotalSummaryViews>0</TotalSummaryViews>
                <TotalDesktopSummaryViews>0</TotalDesktopSummaryViews>
                <TotalMobileSummaryViews>0</TotalMobileSummaryViews>
                <TotalDetailViews>0</TotalDetailViews>
                <TotalDesktopDetailViews>0</TotalDesktopDetailViews>
                <TotalMobileDetailViews>0</TotalMobileDetailViews>
            </ItpPropertyAdvert>
        </PropertyAdverts>
        <RightMoveUrl>http://www.adftest.rightmove.com/property-to-rent/property-56842607.html</RightMoveUrl>
        <RightMoveRef>1f5c2822-5284-445d-80ef-cee4d555900d__Test1__</RightMoveRef>
        <KeyFeatures list="true">
            <ItpPropertyKeyFeature>
                <Value>We accept DSS applicants, families with children, pets and students.</Value>
            </ItpPropertyKeyFeature>
            <ItpPropertyKeyFeature>
                <Value>Property has communal and front gardens.</Value>
            </ItpPropertyKeyFeature>
            <ItpPropertyKeyFeature>
                <Value>Property has gas and oil heating.</Value>
            </ItpPropertyKeyFeature>
            <ItpPropertyKeyFeature>
                <Value>Parking - allocated and garage.</Value>
            </ItpPropertyKeyFeature>
            <ItpPropertyKeyFeature>
                <Value>60 months term.</Value>
            </ItpPropertyKeyFeature>
        </KeyFeatures>
        <DisplayAddress>Mountain Road, Hayes, Middlesex</DisplayAddress>
        <WorkOrders/>
        <ExternalPayments/>
    </Property>
    <Tenancy>
        <TenancyId>ea690283-70bb-4ea7-afde-a005de8d9412</TenancyId>
        <RentAmount>1000.00</RentAmount>
        <RentAmountInAdvance>1000.00</RentAmountInAdvance>
        <RentDueDate>2016-05-15T00:00:00</RentDueDate>
        <OccupancyLength>60</OccupancyLength>
        <StartDate>2016-04-15T00:00:00</StartDate>
        <EndDate>2021-04-14T23:59:59</EndDate>
        <GuarantorAccept>true</GuarantorAccept>
        <DepositAmount>1000.00</DepositAmount>
        <RentRemainingAmount>0.00</RentRemainingAmount>
        <RentRecievedAmount>0.00</RentRecievedAmount>
        <UtilitiesRecievedAmount>0.00</UtilitiesRecievedAmount>
        <DepositSchemeType>
            <Value>None</Value>
            <Description>None</Description>
            <Id>0</Id>
        </DepositSchemeType>
        <TotalMoveInMonies>2000.00</TotalMoveInMonies>
        <MoveInMoniesPaid>false</MoveInMoniesPaid>
        <SpecialTerms list="true">
            <ItpSpecialTerm>
                <SpecialTermType>
                    <Value>NoSmokingAllowed</Value>
                    <Description>No smoking inside the building(s)</Description>
                    <Id>5</Id>
                </SpecialTermType>
                <Description>No smoking inside the building(s)</Description>
            </ItpSpecialTerm>
            <ItpSpecialTerm>
                <SpecialTermType>
                    <Value>Other</Value>
                    <Description>Other (See Text)</Description>
                    <Id>1</Id>
                </SpecialTermType>
                <Description>Access to Loft</Description>
            </ItpSpecialTerm>
        </SpecialTerms>
        <BankAccountForPayments>
            <AccountName>My Account</AccountName>
            <AccountNumber>12345678</AccountNumber>
            <BankName>Barclays</BankName>
            <SortCode>10-11-12</SortCode>
        </BankAccountForPayments>
        <WallMessages/>
        <Occupants/>
        <AwaitingAgreementCreation>true</AwaitingAgreementCreation>
        <ReferencePaymentHoursRemaining>0</ReferencePaymentHoursRemaining>
        <AgreementHoursRemaining>80</AgreementHoursRemaining>
        <TenancyDocuments list="true">
            <ItpTenancyDocument>
                <DocumentName>ref-Inventory</DocumentName>
                <DocumentUrl>https://project-equalet-documents.s3.amazonaws.com/Test1/ea690283-70bb-4ea7-afde-a005de8d9412/Documents/20160215121809982.pdf</DocumentUrl>
                <DocumentType>Inventory</DocumentType>
                <DocumentDate xsi:nil="true"/>
            </ItpTenancyDocument>
            <ItpTenancyDocument>
                <DocumentName>CreditReport-21 Mountain Road-20160215121822404.html</DocumentName>
                <DocumentUrl>https://project-equalet-documents.s3.amazonaws.com/Test1/1f33ded2-c07d-45a5-be6a-08328194f0f5/Documents/CreditReport-21MountainRoad-20160215121822404.html</DocumentUrl>
                <DocumentType>CreditCheckReport</DocumentType>
                <DocumentDate>2016-02-15T12:18:22.45</DocumentDate>
            </ItpTenancyDocument>
        </TenancyDocuments>
    </Tenancy>
    <PropertyUsers list="true">
        <ItpUser>
            <UserId>1f33ded2-c07d-45a5-be6a-08328194f0f5</UserId>
            <Title>Dr</Title>
            <FirstName>Harold</FirstName>
            <LastName>Chrysler</LastName>
            <Email>trishiblet@9yds-testing.co.uk</Email>
            <HomeTel>474581889</HomeTel>
            <WorkTel>1042066969</WorkTel>
            <Mobile>200680493</Mobile>
            <PropertyUserType>
                <Value>ManuallyInvitedTenant</Value>
                <Description>Tenant</Description>
                <Id>4</Id>
            </PropertyUserType>
            <Addresses list="true">
                <ItpAddress>
                    <AddressId>5f547622-ded3-e511-81e6-06ab496445e9</AddressId>
                    <AddressLine1>18, Top Gear Lane</AddressLine1>
                    <City>Test Town</City>
                    <Postcode>X9 9LF</Postcode>
                    <CurrentAddress>true</CurrentAddress>
                    <ResidencyStatus>PrivateRented</ResidencyStatus>
                    <ResidencyStatusDesc>Private Rented</ResidencyStatusDesc>
                </ItpAddress>
            </Addresses>
            <IdCheckStatus>
                <Value>Passed</Value>
                <Description>ID matched and ID Check Passed</Description>
                <Id>1</Id>
            </IdCheckStatus>
            <NextOfKin>
                <Name>Ted Accountant</Name>
                <TelephoneNumber>01234 567891</TelephoneNumber>
                <Email>test@test.com</Email>
                <ContactAddress>
                    <AddressId>babca730-ded3-e511-81e6-06ab496445e9</AddressId>
                    <AddressLine1>UserAddress 1</AddressLine1>
                    <AddressLine2>UserAddress 2</AddressLine2>
                    <City>City</City>
                    <County>County</County>
                    <Postcode>PO5 8DE</Postcode>
                    <Country>Country</Country>
                    <CurrentAddress>true</CurrentAddress>
                    <ResidencyStatus>NotSet</ResidencyStatus>
                    <ResidencyStatusDesc>Unknown</ResidencyStatusDesc>
                </ContactAddress>
            </NextOfKin>
            <UserDocuments list="true">
                <ItpDocument>
                    <Url>https://project-equalet-documents.s3.amazonaws.com/Test1/1f33ded2-c07d-45a5-be6a-08328194f0f5/Documents/CreditReport-21MountainRoad-20160215121822404.html</Url>
                    <DocumentType>CreditCheckReport</DocumentType>
                    <DocumentReference>CreditReport-21 Mountain Road-20160215121822404.html</DocumentReference>
                    <DocumentDate>2016-02-15T12:18:22.45</DocumentDate>
                    <StartDate xsi:nil="true"/>
                    <EndDate xsi:nil="true"/>
                    <Verified>true</Verified>
                </ItpDocument>
                <ItpDocument>
                    <Url>https://project-equalet-documents.s3.amazonaws.com/Test1/1f33ded2-c07d-45a5-be6a-08328194f0f5/Documents/IdCheckReport-0.html</Url>
                    <DocumentType>IdCheckReport</DocumentType>
                    <DocumentReference>IdCheckReport-0.html</DocumentReference>
                    <DocumentDate>2016-02-15T12:17:56.763</DocumentDate>
                    <StartDate xsi:nil="true"/>
                    <EndDate xsi:nil="true"/>
                    <Verified>true</Verified>
                </ItpDocument>
                <ItpDocument>
                    <Url>https://project-equalet-documents.s3.amazonaws.com/Test1/1f33ded2-c07d-45a5-be6a-08328194f0f5/Documents/20160215121832747.pdf</Url>
                    <DocumentType>ProofOfResidence</DocumentType>
                    <DocumentReference>ref-ProofOfResidence</DocumentReference>
                    <DocumentDate xsi:nil="true"/>
                    <StartDate>2015-02-15T12:18:21.987</StartDate>
                    <EndDate>2017-02-15T12:18:21.987</EndDate>
                    <Verified>true</Verified>
                </ItpDocument>
                <ItpDocument>
                    <Url>https://project-equalet-documents.s3.amazonaws.com/Test1/1f33ded2-c07d-45a5-be6a-08328194f0f5/Documents/20160215121832950.pdf</Url>
                    <DocumentType>PhotoId</DocumentType>
                    <DocumentReference>ref-PhotoId</DocumentReference>
                    <DocumentDate xsi:nil="true"/>
                    <StartDate>2015-02-15T12:18:22.207</StartDate>
                    <EndDate>2017-02-15T12:18:22.207</EndDate>
                    <Verified>true</Verified>
                </ItpDocument>
                <ItpDocument>
                    <Url>https://project-equalet-documents.s3.amazonaws.com/Test1/1f33ded2-c07d-45a5-be6a-08328194f0f5/Documents/20160215121833700.pdf</Url>
                    <DocumentType>ImmigrationStatusDoc</DocumentType>
                    <DocumentReference>ref-ImmigrationStatusDoc</DocumentReference>
                    <DocumentDate xsi:nil="true"/>
                    <StartDate>2015-02-15T12:18:22.963</StartDate>
                    <EndDate>2017-02-15T12:18:22.963</EndDate>
                    <Verified>true</Verified>
                </ItpDocument>
            </UserDocuments>
            <ControllingOrganisation>
                <OrganisationStatus>Limited</OrganisationStatus>
                <OrganisationType>Advertising</OrganisationType>
                <RegisteredOrganisationName>TrisHibLet Ltd</RegisteredOrganisationName>
                <TradingName>TrisHibLet</TradingName>
                <LogoUrl>http://images.TestLettings.Property-Portal.uk/b2b/hiblenlets.gif</LogoUrl>
                <RegistrationNumber>11111111</RegistrationNumber>
                <VatNumber>928289676x</VatNumber>
                <CompanyTelephone>0333 006 3000x</CompanyTelephone>
                <CompanyEmail>theteam@TrisHibLet.co.uk</CompanyEmail>
                <Established>2015-10-01T00:00:00</Established>
                <GrossProfit>0.00</GrossProfit>
                <MarketingType>
                    <Value>NoMarketing</Value>
                    <Description>NoMarketing</Description>
                    <Id>2</Id>
                </MarketingType>
                <ShowCoBranding>true</ShowCoBranding>
                <OrganisationUsers list="true">
                    <ItpOrganisationUser>
                        <OrganisationUserType>
                            <Value>OrganisationAdministrator</Value>
                            <Description>Organisation Administrator</Description>
                            <Id>1</Id>
                        </OrganisationUserType>
                        <OrganisationUserRole>
                            <Value>Owner</Value>
                            <Description>Owner</Description>
                            <Id>1</Id>
                        </OrganisationUserRole>
                        <SigningAuthority>true</SigningAuthority>
                        <Contact>
                            <Name>Harold Chrysler</Name>
                            <TelephoneNumber>200680493</TelephoneNumber>
                            <Email>trishiblet@9yds-testing.co.uk</Email>
                            <ContactAddress>
                                <AddressId>5f547622-ded3-e511-81e6-06ab496445e9</AddressId>
                                <AddressLine1>18, Top Gear Lane</AddressLine1>
                                <City>Test Town</City>
                                <Postcode>X9 9LF</Postcode>
                                <CurrentAddress>true</CurrentAddress>
                                <ResidencyStatus>PrivateRented</ResidencyStatus>
                                <ResidencyStatusDesc>Private Rented</ResidencyStatusDesc>
                            </ContactAddress>
                        </Contact>
                    </ItpOrganisationUser>
                    <ItpOrganisationUser>
                        <OrganisationUserType>
                            <Value>OrganisationAdministrator</Value>
                            <Description>Organisation Administrator</Description>
                            <Id>1</Id>
                        </OrganisationUserType>
                        <OrganisationUserRole>
                            <Value>Owner</Value>
                            <Description>Owner</Description>
                            <Id>1</Id>
                        </OrganisationUserRole>
                        <SigningAuthority>true</SigningAuthority>
                        <Contact>
                            <Name>Org Admin</Name>
                            <Email>TrisHibLet@hiblen.com</Email>
                        </Contact>
                    </ItpOrganisationUser>
                </OrganisationUsers>
                <Addresses list="true">
                    <ItpAddress>
                        <AddressId>7f5d7904-68d1-e511-81e5-06ab496445e9</AddressId>
                        <AddressLine1>TrisHibLet</AddressLine1>
                        <AddressLine2>PO box 666</AddressLine2>
                        <City>London</City>
                        <Postcode>SW12 9KL</Postcode>
                        <CurrentAddress>true</CurrentAddress>
                        <ResidencyStatus>Owned</ResidencyStatus>
                        <AddressType>
                            <Value>RegisteredOffice</Value>
                            <Description>RegisteredOffice</Description>
                            <Id>2</Id>
                        </AddressType>
                        <ResidencyStatusDesc>Owned</ResidencyStatusDesc>
                    </ItpAddress>
                    <ItpAddress>
                        <AddressId>805d7904-68d1-e511-81e5-06ab496445e9</AddressId>
                        <AddressLine1>TrisHibLet</AddressLine1>
                        <AddressLine2>PO box 666</AddressLine2>
                        <City>London</City>
                        <Postcode>SW12 9KL</Postcode>
                        <CurrentAddress>true</CurrentAddress>
                        <ResidencyStatus>Owned</ResidencyStatus>
                        <AddressType>
                            <Value>AccountantAddress</Value>
                            <Description>AccountantAddress</Description>
                            <Id>4</Id>
                        </AddressType>
                        <ResidencyStatusDesc>Owned</ResidencyStatusDesc>
                    </ItpAddress>
                </Addresses>
                <BankAccounts list="true">
                    <ItpBank/>
                </BankAccounts>
            </ControllingOrganisation>
            <LandlordType>
                <Value>NotSet</Value>
                <Description>NotSet</Description>
                <Id>0</Id>
            </LandlordType>
            <ReferencingPaid>true</ReferencingPaid>
            <ReferenceCheckStatus>Passed</ReferenceCheckStatus>
            <ReferenceCheckSoftPass>false</ReferenceCheckSoftPass>
            <GuarantorRequired xsi:nil="true"/>
            <GuarantorAdded>false</GuarantorAdded>
            <AgreementSigningStatus>NotSet</AgreementSigningStatus>
            <ConfirmedUser>true</ConfirmedUser>
            <SigningUser>true</SigningUser>
            <AgencyStaff>true</AgencyStaff>
            <NoPasswordEnteredOnRegistration>false</NoPasswordEnteredOnRegistration>
            <TenantWantsDetails>false</TenantWantsDetails>
            <TenantWantsViewing>false</TenantWantsViewing>
            <IsSmoker>false</IsSmoker>
            <HasPets>true</HasPets>
            <HasDependents>true</HasDependents>
            <IsRegisteringDeposit>false</IsRegisteringDeposit>
        </ItpUser>
        <ItpUser>
            <UserId>f1eed456-2530-4ab9-af63-2bc37a7b0d5d</UserId>
            <Title>Dr</Title>
            <FirstName>Sadie</FirstName>
            <LastName>Griffin</LastName>
            <Email>prime_LL20@9yds-testing.co.uk</Email>
            <HomeTel>2101007003</HomeTel>
            <WorkTel>745218734</WorkTel>
            <Mobile>605170075</Mobile>
            <PropertyUserType>
                <Value>PropertyOwner</Value>
                <Description>Property Administrator</Description>
                <Id>1</Id>
            </PropertyUserType>
            <Addresses list="true">
                <ItpAddress>
                    <AddressId>abce465a-d3d3-e511-81e6-06ab496445e9</AddressId>
                    <AddressLine1>20 Mountain Road</AddressLine1>
                    <City>Hayes</City>
                    <Postcode>UB3 4RB</Postcode>
                    <CurrentAddress>true</CurrentAddress>
                    <ResidencyStatus>NotSet</ResidencyStatus>
                    <ResidencyStatusDesc>NotSet</ResidencyStatusDesc>
                </ItpAddress>
            </Addresses>
            <IdCheckStatus>
                <Value>NotChecked</Value>
                <Description>ID Check not yet Performed</Description>
                <Id>0</Id>
            </IdCheckStatus>
            <UserDocuments list="true">
                <ItpDocument>
                    <Url>https://project-equalet-documents.s3.amazonaws.com/Test1/f1eed456-2530-4ab9-af63-2bc37a7b0d5d/Documents/20160215111920054.pdf</Url>
                    <DocumentType>ProofOfResidence</DocumentType>
                    <DocumentReference>ref-ProofOfResidence</DocumentReference>
                    <DocumentDate xsi:nil="true"/>
                    <StartDate>2015-02-12T11:19:09.09</StartDate>
                    <EndDate>2015-02-14T11:19:09.09</EndDate>
                    <Verified>true</Verified>
                </ItpDocument>
                <ItpDocument>
                    <Url>https://project-equalet-documents.s3.amazonaws.com/Test1/f1eed456-2530-4ab9-af63-2bc37a7b0d5d/Documents/20160215111920304.pdf</Url>
                    <DocumentType>PhotoId</DocumentType>
                    <DocumentReference>ref-PhotoId</DocumentReference>
                    <DocumentDate xsi:nil="true"/>
                    <StartDate>2015-02-12T11:19:09.537</StartDate>
                    <EndDate>2015-02-14T11:19:09.537</EndDate>
                    <Verified>true</Verified>
                </ItpDocument>
                <ItpDocument>
                    <Url>https://project-equalet-documents.s3.amazonaws.com/Test1/f1eed456-2530-4ab9-af63-2bc37a7b0d5d/Documents/20160215121805748.pdf</Url>
                    <DocumentType>ProofOfResidence</DocumentType>
                    <DocumentReference>ref-ProofOfResidence</DocumentReference>
                    <DocumentDate xsi:nil="true"/>
                    <StartDate>2015-02-15T12:17:54.903</StartDate>
                    <EndDate>2017-02-15T12:17:54.903</EndDate>
                    <Verified>true</Verified>
                </ItpDocument>
                <ItpDocument>
                    <Url>https://project-equalet-documents.s3.amazonaws.com/Test1/f1eed456-2530-4ab9-af63-2bc37a7b0d5d/Documents/20160215121806513.pdf</Url>
                    <DocumentType>PhotoId</DocumentType>
                    <DocumentReference>ref-PhotoId</DocumentReference>
                    <DocumentDate xsi:nil="true"/>
                    <StartDate>2015-02-15T12:17:55.757</StartDate>
                    <EndDate>2017-02-15T12:17:55.757</EndDate>
                    <Verified>true</Verified>
                </ItpDocument>
            </UserDocuments>
            <ControllingOrganisation>
                <OrganisationStatus>Limited</OrganisationStatus>
                <OrganisationType>Advertising</OrganisationType>
                <RegisteredOrganisationName>Glanty Ltd</RegisteredOrganisationName>
                <TradingName>9yds</TradingName>
                <LogoUrl>https://prime.9yds.co.uk/assets/images/9yds_navbar_logo.png</LogoUrl>
                <RegistrationNumber>05562443</RegistrationNumber>
                <VatNumber>928289676</VatNumber>
                <CompanyTelephone>0333 006 3000</CompanyTelephone>
                <CompanyEmail>theteam@9yds.co.uk</CompanyEmail>
                <Established>2005-01-01T00:00:00</Established>
                <GrossProfit>0.00</GrossProfit>
                <MarketingType>
                    <Value>PropertyPortal</Value>
                    <Description>PropertyPortal</Description>
                    <Id>1</Id>
                </MarketingType>
                <ShowCoBranding>false</ShowCoBranding>
                <OrganisationUsers list="true">
                    <ItpOrganisationUser>
                        <OrganisationUserType>
                            <Value>OrganisationAdministrator</Value>
                            <Description>Organisation Administrator</Description>
                            <Id>1</Id>
                        </OrganisationUserType>
                        <OrganisationUserRole>
                            <Value>Partner</Value>
                            <Description>Partner</Description>
                            <Id>2</Id>
                        </OrganisationUserRole>
                        <SigningAuthority>true</SigningAuthority>
                        <Contact>
                            <Name>Prime Test</Name>
                            <Email>primeadmin@9yds-testing.co.uk</Email>
                        </Contact>
                    </ItpOrganisationUser>
                </OrganisationUsers>
                <Addresses list="true">
                    <ItpAddress>
                        <AddressId>785d7904-68d1-e511-81e5-06ab496445e9</AddressId>
                        <AddressLine1>9yds</AddressLine1>
                        <AddressLine2>PO box 459</AddressLine2>
                        <City>Gravesend</City>
                        <Postcode>DA12 9JW</Postcode>
                        <CurrentAddress>true</CurrentAddress>
                        <ResidencyStatus>Owned</ResidencyStatus>
                        <AddressType>
                            <Value>RegisteredOffice</Value>
                            <Description>RegisteredOffice</Description>
                            <Id>2</Id>
                        </AddressType>
                        <ResidencyStatusDesc>Owned</ResidencyStatusDesc>
                    </ItpAddress>
                    <ItpAddress>
                        <AddressId>795d7904-68d1-e511-81e5-06ab496445e9</AddressId>
                        <AddressLine1>9yds</AddressLine1>
                        <AddressLine2>PO box 459</AddressLine2>
                        <City>Gravesend</City>
                        <Postcode>DA12 9JW</Postcode>
                        <CurrentAddress>true</CurrentAddress>
                        <ResidencyStatus>Owned</ResidencyStatus>
                        <AddressType>
                            <Value>AccountantAddress</Value>
                            <Description>AccountantAddress</Description>
                            <Id>4</Id>
                        </AddressType>
                        <ResidencyStatusDesc>Owned</ResidencyStatusDesc>
                    </ItpAddress>
                </Addresses>
                <BankAccounts list="true">
                    <ItpBank/>
                </BankAccounts>
            </ControllingOrganisation>
            <LandlordType>
                <Value>UnManagedPropertyAdministrator</Value>
                <Description>Where a property administrator registers with the site directly</Description>
                <Id>3</Id>
            </LandlordType>
            <ReferencingPaid xsi:nil="true"/>
            <ReferenceCheckStatus>NotChecked</ReferenceCheckStatus>
            <ReferenceCheckSoftPass xsi:nil="true"/>
            <GuarantorRequired xsi:nil="true"/>
            <GuarantorAdded xsi:nil="true"/>
            <AgreementSigningStatus>NotSet</AgreementSigningStatus>
            <ConfirmedUser>true</ConfirmedUser>
            <SigningUser>true</SigningUser>
            <AgencyStaff>false</AgencyStaff>
            <NoPasswordEnteredOnRegistration>false</NoPasswordEnteredOnRegistration>
            <TenantWantsDetails>false</TenantWantsDetails>
            <TenantWantsViewing>false</TenantWantsViewing>
            <IsSmoker>false</IsSmoker>
            <HasPets>false</HasPets>
            <HasDependents>false</HasDependents>
            <IsRegisteringDeposit>true</IsRegisteringDeposit>
        </ItpUser>
    </PropertyUsers>
</ItpDocumentRequest>
'''


xml1 = '''
<ItpDocumentRequest xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <DocumentCode>AgreementTimerExtended</DocumentCode>
    <UrlLinks list="true">
        <ItpUrlLink>
            <LinkType>AppUrl</LinkType>
            <LinkUrl>http://TrisHibLet.Test1Lettings.Property-Portal.uk:81/</LinkUrl>
        </ItpUrlLink>
        <ItpUrlLink>
            <LinkType>ImageStore</LinkType>
            <LinkUrl>http://Images.TestLettings.Property-Portal.uk/</LinkUrl>
        </ItpUrlLink>
    </UrlLinks>
    <AppUrl>http://TrisHibLet.Test1Lettings.Property-Portal.uk:81/</AppUrl>
    <EMailUser>
        <UserId>1f33ded2-c07d-45a5-be6a-08328194f0f5</UserId>
        <Title>Dr</Title>
        <FirstName>Harold</FirstName>
        <LastName>Chrysler</LastName>
        <Email>trishiblet@9yds-testing.co.uk</Email>
        <HomeTel>474581889</HomeTel>
        <WorkTel>1042066969</WorkTel>
        <Mobile>200680493</Mobile>
        <PropertyUserType>
            <Value>ManuallyInvitedTenant</Value>
            <Description>Tenant</Description>
            <Id>4</Id>
        </PropertyUserType>
        <Addresses list="true">
            <ItpAddress>
                <AddressId>5f547622-ded3-e511-81e6-06ab496445e9</AddressId>
                <AddressLine1>18, Top Gear Lane</AddressLine1>
                <City>Test Town</City>
                <Postcode>X9 9LF</Postcode>
                <CurrentAddress>true</CurrentAddress>
                <ResidencyStatus>PrivateRented</ResidencyStatus>
                <ResidencyStatusDesc>Private Rented</ResidencyStatusDesc>
            </ItpAddress>
        </Addresses>
        <IdCheckStatus>
            <Value>Passed</Value>
            <Description>ID matched and ID Check Passed</Description>
            <Id>1</Id>
        </IdCheckStatus>
        <NextOfKin>
            <Name>Ted Accountant</Name>
            <TelephoneNumber>01234 567891</TelephoneNumber>
            <Email>test@test.com</Email>
            <ContactAddress>
                <AddressId>babca730-ded3-e511-81e6-06ab496445e9</AddressId>
                <AddressLine1>UserAddress 1</AddressLine1>
                <AddressLine2>UserAddress 2</AddressLine2>
                <City>City</City>
                <County>County</County>
                <Postcode>PO5 8DE</Postcode>
                <Country>Country</Country>
                <CurrentAddress>true</CurrentAddress>
                <ResidencyStatus>NotSet</ResidencyStatus>
                <ResidencyStatusDesc>Unknown</ResidencyStatusDesc>
            </ContactAddress>
        </NextOfKin>
        <UserDocuments list="true">
            <ItpDocument>
                <Url>https://project-equalet-documents.s3.amazonaws.com/Test1/1f33ded2-c07d-45a5-be6a-08328194f0f5/Documents/CreditReport-21MeridianRoad-20160215121822404.html</Url>
                <DocumentType>CreditCheckReport</DocumentType>
                <DocumentReference>CreditReport-21 Meridian Road-20160215121822404.html</DocumentReference>
                <DocumentDate>2016-02-15T12:18:22.45</DocumentDate>
                <StartDate xsi:nil="true"/>
                <EndDate xsi:nil="true"/>
                <Verified>true</Verified>
            </ItpDocument>
            <ItpDocument>
                <Url>https://project-equalet-documents.s3.amazonaws.com/Test1/1f33ded2-c07d-45a5-be6a-08328194f0f5/Documents/IdCheckReport-0.html</Url>
                <DocumentType>IdCheckReport</DocumentType>
                <DocumentReference>IdCheckReport-0.html</DocumentReference>
                <DocumentDate>2016-02-15T12:17:56.763</DocumentDate>
                <StartDate xsi:nil="true"/>
                <EndDate xsi:nil="true"/>
                <Verified>true</Verified>
            </ItpDocument>
            <ItpDocument>
                <Url>https://project-equalet-documents.s3.amazonaws.com/Test1/1f33ded2-c07d-45a5-be6a-08328194f0f5/Documents/20160215121832747.pdf</Url>
                <DocumentType>ProofOfResidence</DocumentType>
                <DocumentReference>ref-ProofOfResidence</DocumentReference>
                <DocumentDate xsi:nil="true"/>
                <StartDate>2015-02-15T12:18:21.987</StartDate>
                <EndDate>2017-02-15T12:18:21.987</EndDate>
                <Verified>true</Verified>
            </ItpDocument>
            <ItpDocument>
                <Url>https://project-equalet-documents.s3.amazonaws.com/Test1/1f33ded2-c07d-45a5-be6a-08328194f0f5/Documents/20160215121832950.pdf</Url>
                <DocumentType>PhotoId</DocumentType>
                <DocumentReference>ref-PhotoId</DocumentReference>
                <DocumentDate xsi:nil="true"/>
                <StartDate>2015-02-15T12:18:22.207</StartDate>
                <EndDate>2017-02-15T12:18:22.207</EndDate>
                <Verified>true</Verified>
            </ItpDocument>
            <ItpDocument>
                <Url>https://project-equalet-documents.s3.amazonaws.com/Test1/1f33ded2-c07d-45a5-be6a-08328194f0f5/Documents/20160215121833700.pdf</Url>
                <DocumentType>ImmigrationStatusDoc</DocumentType>
                <DocumentReference>ref-ImmigrationStatusDoc</DocumentReference>
                <DocumentDate xsi:nil="true"/>
                <StartDate>2015-02-15T12:18:22.963</StartDate>
                <EndDate>2017-02-15T12:18:22.963</EndDate>
                <Verified>true</Verified>
            </ItpDocument>
        </UserDocuments>
        <ControllingOrganisation>
            <OrganisationStatus>Limited</OrganisationStatus>
            <OrganisationType>Advertising</OrganisationType>
            <RegisteredOrganisationName>TrisHibLet Ltd</RegisteredOrganisationName>
            <TradingName>TrisHibLet</TradingName>
            <LogoUrl>http://images.TestLettings.Property-Portal.uk/b2b/hiblenlets.gif</LogoUrl>
            <RegistrationNumber>11111111</RegistrationNumber>
            <VatNumber>928289676x</VatNumber>
            <CompanyTelephone>0333 006 3000x</CompanyTelephone>
            <CompanyEmail>theteam@TrisHibLet.co.uk</CompanyEmail>
            <Established>2015-10-01T00:00:00</Established>
            <GrossProfit>0.00</GrossProfit>
            <MarketingType>
                <Value>NoMarketing</Value>
                <Description>NoMarketing</Description>
                <Id>2</Id>
            </MarketingType>
            <ShowCoBranding>true</ShowCoBranding>
            <OrganisationUsers list="true">
                <ItpOrganisationUser>
                    <OrganisationUserType>
                        <Value>OrganisationAdministrator</Value>
                        <Description>Organisation Administrator</Description>
                        <Id>1</Id>
                    </OrganisationUserType>
                    <OrganisationUserRole>
                        <Value>Owner</Value>
                        <Description>Owner</Description>
                        <Id>1</Id>
                    </OrganisationUserRole>
                    <SigningAuthority>true</SigningAuthority>
                    <Contact>
                        <Name>Harold Chrysler</Name>
                        <TelephoneNumber>200680493</TelephoneNumber>
                        <Email>trishiblet@9yds-testing.co.uk</Email>
                        <ContactAddress>
                            <AddressId>5f547622-ded3-e511-81e6-06ab496445e9</AddressId>
                            <AddressLine1>18, Top Gear Lane</AddressLine1>
                            <City>Test Town</City>
                            <Postcode>X9 9LF</Postcode>
                            <CurrentAddress>true</CurrentAddress>
                            <ResidencyStatus>PrivateRented</ResidencyStatus>
                            <ResidencyStatusDesc>Private Rented</ResidencyStatusDesc>
                        </ContactAddress>
                    </Contact>
                </ItpOrganisationUser>
                <ItpOrganisationUser>
                    <OrganisationUserType>
                        <Value>OrganisationAdministrator</Value>
                        <Description>Organisation Administrator</Description>
                        <Id>1</Id>
                    </OrganisationUserType>
                    <OrganisationUserRole>
                        <Value>Owner</Value>
                        <Description>Owner</Description>
                        <Id>1</Id>
                    </OrganisationUserRole>
                    <SigningAuthority>true</SigningAuthority>
                    <Contact>
                        <Name>Org Admin</Name>
                        <Email>TrisHibLet@hiblen.com</Email>
                    </Contact>
                </ItpOrganisationUser>
            </OrganisationUsers>
            <Addresses list="true">
                <ItpAddress>
                    <AddressId>7f5d7904-68d1-e511-81e5-06ab496445e9</AddressId>
                    <AddressLine1>TrisHibLet</AddressLine1>
                    <AddressLine2>PO box 666</AddressLine2>
                    <City>London</City>
                    <Postcode>SW12 9KL</Postcode>
                    <CurrentAddress>true</CurrentAddress>
                    <ResidencyStatus>Owned</ResidencyStatus>
                    <AddressType>
                        <Value>RegisteredOffice</Value>
                        <Description>RegisteredOffice</Description>
                        <Id>2</Id>
                    </AddressType>
                    <ResidencyStatusDesc>Owned</ResidencyStatusDesc>
                </ItpAddress>
                <ItpAddress>
                    <AddressId>805d7904-68d1-e511-81e5-06ab496445e9</AddressId>
                    <AddressLine1>TrisHibLet</AddressLine1>
                    <AddressLine2>PO box 666</AddressLine2>
                    <City>London</City>
                    <Postcode>SW12 9KL</Postcode>
                    <CurrentAddress>true</CurrentAddress>
                    <ResidencyStatus>Owned</ResidencyStatus>
                    <AddressType>
                        <Value>AccountantAddress</Value>
                        <Description>AccountantAddress</Description>
                        <Id>4</Id>
                    </AddressType>
                    <ResidencyStatusDesc>Owned</ResidencyStatusDesc>
                </ItpAddress>
            </Addresses>
            <BankAccounts list="true">
                <ItpBank/>
            </BankAccounts>
        </ControllingOrganisation>
        <LandlordType>
            <Value>NotSet</Value>
            <Description>NotSet</Description>
            <Id>0</Id>
        </LandlordType>
        <ReferencingPaid>true</ReferencingPaid>
        <ReferenceCheckStatus>Passed</ReferenceCheckStatus>
        <ReferenceCheckSoftPass>false</ReferenceCheckSoftPass>
        <GuarantorRequired xsi:nil="true"/>
        <GuarantorAdded>false</GuarantorAdded>
        <AgreementSigningStatus>NotSet</AgreementSigningStatus>
        <ConfirmedUser>true</ConfirmedUser>
        <SigningUser>true</SigningUser>
        <AgencyStaff>true</AgencyStaff>
        <NoPasswordEnteredOnRegistration>false</NoPasswordEnteredOnRegistration>
        <TenantWantsDetails>false</TenantWantsDetails>
        <TenantWantsViewing>false</TenantWantsViewing>
        <IsSmoker>false</IsSmoker>
        <HasPets>true</HasPets>
        <HasDependents>true</HasDependents>
        <IsRegisteringDeposit>false</IsRegisteringDeposit>
    </EMailUser>
    <Property>
        <PropertyId>c0476ede-ddd3-e511-81e6-06ab496445e9</PropertyId>
        <HeatingTypes list="true">
            <ItemOfHeatingType>
                <Value>Gas</Value>
                <Description>Gas</Description>
                <Id>1</Id>
            </ItemOfHeatingType>
            <ItemOfHeatingType>
                <Value>Oil</Value>
                <Description>Oil</Description>
                <Id>4</Id>
            </ItemOfHeatingType>
        </HeatingTypes>
        <Postcode>UB3 4RB</Postcode>
        <Description>Description</Description>
        <PropertyTypeId>
            <Value>House</Value>
            <Description>House</Description>
            <Id>1</Id>
        </PropertyTypeId>
        <PropertyStyleId>
            <Value>Detached</Value>
            <Description>Detached</Description>
            <Id>1</Id>
        </PropertyStyleId>
        <DateAvailable>2016-03-15T00:00:00</DateAvailable>
        <FurnishedId>
            <Value>Partfurnished</Value>
            <Description>Part Furnished</Description>
            <Id>2</Id>
        </FurnishedId>
        <ParkingTypes list="true">
            <ItemOfParkingType>
                <Value>AllocatedParking</Value>
                <Description>Allocated Parking</Description>
                <Id>2</Id>
            </ItemOfParkingType>
            <ItemOfParkingType>
                <Value>Garage</Value>
                <Description>Garage</Description>
                <Id>8</Id>
            </ItemOfParkingType>
        </ParkingTypes>
        <OutsideSpaces list="true">
            <ItemOfOutsideSpaceType>
                <Value>CommunalGarden</Value>
                <Description>Communal Garden</Description>
                <Id>1</Id>
            </ItemOfOutsideSpaceType>
            <ItemOfOutsideSpaceType>
                <Value>FrontGarden</Value>
                <Description>Front Garden</Description>
                <Id>4</Id>
            </ItemOfOutsideSpaceType>
        </OutsideSpaces>
        <StudentsAllowed>true</StudentsAllowed>
        <ContractMonths>60</ContractMonths>
        <TenureId>
            <Value>Freehold</Value>
            <Description>Freehold</Description>
            <Id>1</Id>
        </TenureId>
        <AddressLine1>21 Meridian Road</AddressLine1>
        <City>Hayes</City>
        <County>Middlesex</County>
        <Country>UK</Country>
        <GasSupplied>true</GasSupplied>
        <Balcony>false</Balcony>
        <HasBuildingsInsurance>false</HasBuildingsInsurance>
        <HasContentsInsurance>false</HasContentsInsurance>
        <PropertyImages list="true">
            <ItpPropertyImage>
                <Url>https://project-equalet-documents.s3.amazonaws.com/Test1/c0476ede-ddd3-e511-81e6-06ab496445e9/Photos/20160215121559173.jpg</Url>
            </ItpPropertyImage>
        </PropertyImages>
        <PropertyDocuments list="true">
            <ItpDocument>
                <Url>https://project-equalet-documents.s3.amazonaws.com/Test1/c0476ede-ddd3-e511-81e6-06ab496445e9/Documents/20160215121808482.pdf</Url>
                <DocumentType>Epc</DocumentType>
                <DocumentReference>ref-Epc</DocumentReference>
                <DocumentDate xsi:nil="true"/>
                <StartDate>2015-02-15T12:17:57.74</StartDate>
                <EndDate>2017-02-15T12:17:57.74</EndDate>
                <Verified>true</Verified>
            </ItpDocument>
            <ItpDocument>
                <Url>https://project-equalet-documents.s3.amazonaws.com/Test1/c0476ede-ddd3-e511-81e6-06ab496445e9/Documents/20160215121808795.pdf</Url>
                <DocumentType>GasSafety</DocumentType>
                <DocumentReference>ref-GasSafety</DocumentReference>
                <DocumentDate xsi:nil="true"/>
                <StartDate>2015-02-15T12:17:58.047</StartDate>
                <EndDate>2017-02-15T12:17:58.047</EndDate>
                <Verified>true</Verified>
            </ItpDocument>
            <ItpDocument>
                <Url>https://project-equalet-documents.s3.amazonaws.com/Test1/c0476ede-ddd3-e511-81e6-06ab496445e9/Documents/20160215121809670.pdf</Url>
                <DocumentType>ProofOfOwnership</DocumentType>
                <DocumentReference>ref-ProofOfOwnership</DocumentReference>
                <DocumentDate xsi:nil="true"/>
                <StartDate>2015-02-15T12:17:58.923</StartDate>
                <EndDate>2017-02-15T12:17:58.923</EndDate>
                <Verified>true</Verified>
            </ItpDocument>
        </PropertyDocuments>
        <PropertyRooms list="true">
            <ItpPropertyRoom>
                <RoomTypeId>
                    <Value>Kitchen</Value>
                    <Description>Kitchen</Description>
                    <Id>7</Id>
                </RoomTypeId>
                <Quantity>1</Quantity>
                <Name>Kitchen</Name>
            </ItpPropertyRoom>
            <ItpPropertyRoom>
                <RoomTypeId>
                    <Value>Bedroom</Value>
                    <Description>Bedroom</Description>
                    <Id>1</Id>
                </RoomTypeId>
                <Quantity>3</Quantity>
                <Name>Bedroom</Name>
            </ItpPropertyRoom>
            <ItpPropertyRoom>
                <RoomTypeId>
                    <Value>Cloakroom</Value>
                    <Description>Cloakroom</Description>
                    <Id>4</Id>
                </RoomTypeId>
                <Quantity>2</Quantity>
                <Name>Cloakroom</Name>
            </ItpPropertyRoom>
        </PropertyRooms>
        <PropertyAdverts list="true">
            <ItpPropertyAdvert>
                <ProviderType>
                    <Value>Rightmove</Value>
                    <Description>Rightmove</Description>
                    <Id>1</Id>
                </ProviderType>
                <AdvertUrl>http://www.adftest.rightmove.com/property-to-rent/property-56842607.html</AdvertUrl>
                <AgentRef>1f5c2822-5284-445d-80ef-cee4d555900d__Test1__</AgentRef>
                <AdvertListingStatus>LetAgreed</AdvertListingStatus>
                <FirstListedDate>2016-02-15T12:16:58</FirstListedDate>
                <TotalSummaryViews>0</TotalSummaryViews>
                <TotalDesktopSummaryViews>0</TotalDesktopSummaryViews>
                <TotalMobileSummaryViews>0</TotalMobileSummaryViews>
                <TotalDetailViews>0</TotalDetailViews>
                <TotalDesktopDetailViews>0</TotalDesktopDetailViews>
                <TotalMobileDetailViews>0</TotalMobileDetailViews>
            </ItpPropertyAdvert>
        </PropertyAdverts>
        <RightMoveUrl>http://www.adftest.rightmove.com/property-to-rent/property-56842607.html</RightMoveUrl>
        <RightMoveRef>1f5c2822-5284-445d-80ef-cee4d555900d__Test1__</RightMoveRef>
        <KeyFeatures list="true">
            <ItpPropertyKeyFeature>
                <Value>We accept DSS applicants, families with children, pets and students.</Value>
            </ItpPropertyKeyFeature>
            <ItpPropertyKeyFeature>
                <Value>Property has communal and front gardens.</Value>
            </ItpPropertyKeyFeature>
            <ItpPropertyKeyFeature>
                <Value>Property has gas and oil heating.</Value>
            </ItpPropertyKeyFeature>
            <ItpPropertyKeyFeature>
                <Value>Parking - allocated and garage.</Value>
            </ItpPropertyKeyFeature>
            <ItpPropertyKeyFeature>
                <Value>60 months term.</Value>
            </ItpPropertyKeyFeature>
        </KeyFeatures>
        <DisplayAddress>Meridian Road, Hayes, Middlesex</DisplayAddress>
        <WorkOrders/>
        <ExternalPayments/>
    </Property>
    <Tenancy>
        <TenancyId>ea690283-70bb-4ea7-afde-a005de8d9412</TenancyId>
        <RentAmount>1000.00</RentAmount>
        <RentAmountInAdvance>1000.00</RentAmountInAdvance>
        <RentDueDate>2016-05-15T00:00:00</RentDueDate>
        <OccupancyLength>60</OccupancyLength>
        <StartDate>2016-04-15T00:00:00</StartDate>
        <EndDate>2021-04-14T23:59:59</EndDate>
        <GuarantorAccept>true</GuarantorAccept>
        <DepositAmount>1000.00</DepositAmount>
        <RentRemainingAmount>0.00</RentRemainingAmount>
        <RentRecievedAmount>0.00</RentRecievedAmount>
        <UtilitiesRecievedAmount>0.00</UtilitiesRecievedAmount>
        <DepositSchemeType>
            <Value>None</Value>
            <Description>None</Description>
            <Id>0</Id>
        </DepositSchemeType>
        <TotalMoveInMonies>2000.00</TotalMoveInMonies>
        <MoveInMoniesPaid>false</MoveInMoniesPaid>
        <SpecialTerms list="true">
            <ItpSpecialTerm>
                <SpecialTermType>
                    <Value>NoSmokingAllowed</Value>
                    <Description>No smoking inside the building(s)</Description>
                    <Id>5</Id>
                </SpecialTermType>
                <Description>No smoking inside the building(s)</Description>
            </ItpSpecialTerm>
            <ItpSpecialTerm>
                <SpecialTermType>
                    <Value>Other</Value>
                    <Description>Other (See Text)</Description>
                    <Id>1</Id>
                </SpecialTermType>
                <Description>Access to Loft</Description>
            </ItpSpecialTerm>
        </SpecialTerms>
        <BankAccountForPayments>
            <AccountName>My Account</AccountName>
            <AccountNumber>12345678</AccountNumber>
            <BankName>Barclays</BankName>
            <SortCode>10-11-12</SortCode>
        </BankAccountForPayments>
        <WallMessages/>
        <Occupants/>
        <AwaitingAgreementCreation>true</AwaitingAgreementCreation>
        <ReferencePaymentHoursRemaining>0</ReferencePaymentHoursRemaining>
        <AgreementHoursRemaining>80</AgreementHoursRemaining>
        <TenancyDocuments list="true">
            <ItpTenancyDocument>
                <DocumentName>ref-Inventory</DocumentName>
                <DocumentUrl>https://project-equalet-documents.s3.amazonaws.com/Test1/ea690283-70bb-4ea7-afde-a005de8d9412/Documents/20160215121809982.pdf</DocumentUrl>
                <DocumentType>Inventory</DocumentType>
                <DocumentDate xsi:nil="true"/>
            </ItpTenancyDocument>
            <ItpTenancyDocument>
                <DocumentName>CreditReport-21 Meridian Road-20160215121822404.html</DocumentName>
                <DocumentUrl>https://project-equalet-documents.s3.amazonaws.com/Test1/1f33ded2-c07d-45a5-be6a-08328194f0f5/Documents/CreditReport-21MeridianRoad-20160215121822404.html</DocumentUrl>
                <DocumentType>CreditCheckReport</DocumentType>
                <DocumentDate>2016-02-15T12:18:22.45</DocumentDate>
            </ItpTenancyDocument>
        </TenancyDocuments>
    </Tenancy>
    <PropertyUsers list="true">
        <ItpUser>
            <UserId>1f33ded2-c07d-45a5-be6a-08328194f0f5</UserId>
            <Title>Dr</Title>
            <FirstName>Harold</FirstName>
            <LastName>Chrysler</LastName>
            <Email>trishiblet@9yds-testing.co.uk</Email>
            <HomeTel>474581889</HomeTel>
            <WorkTel>1042066969</WorkTel>
            <Mobile>200680493</Mobile>
            <PropertyUserType>
                <Value>ManuallyInvitedTenant</Value>
                <Description>Tenant</Description>
                <Id>4</Id>
            </PropertyUserType>
            <Addresses list="true">
                <ItpAddress>
                    <AddressId>5f547622-ded3-e511-81e6-06ab496445e9</AddressId>
                    <AddressLine1>18, Top Gear Lane</AddressLine1>
                    <City>Test Town</City>
                    <Postcode>X9 9LF</Postcode>
                    <CurrentAddress>true</CurrentAddress>
                    <ResidencyStatus>PrivateRented</ResidencyStatus>
                    <ResidencyStatusDesc>Private Rented</ResidencyStatusDesc>
                </ItpAddress>
            </Addresses>
            <IdCheckStatus>
                <Value>Passed</Value>
                <Description>ID matched and ID Check Passed</Description>
                <Id>1</Id>
            </IdCheckStatus>
            <NextOfKin>
                <Name>Ted Accountant</Name>
                <TelephoneNumber>01234 567891</TelephoneNumber>
                <Email>test@test.com</Email>
                <ContactAddress>
                    <AddressId>babca730-ded3-e511-81e6-06ab496445e9</AddressId>
                    <AddressLine1>UserAddress 1</AddressLine1>
                    <AddressLine2>UserAddress 2</AddressLine2>
                    <City>City</City>
                    <County>County</County>
                    <Postcode>PO5 8DE</Postcode>
                    <Country>Country</Country>
                    <CurrentAddress>true</CurrentAddress>
                    <ResidencyStatus>NotSet</ResidencyStatus>
                    <ResidencyStatusDesc>Unknown</ResidencyStatusDesc>
                </ContactAddress>
            </NextOfKin>
            <UserDocuments list="true">
                <ItpDocument>
                    <Url>https://project-equalet-documents.s3.amazonaws.com/Test1/1f33ded2-c07d-45a5-be6a-08328194f0f5/Documents/CreditReport-21MeridianRoad-20160215121822404.html</Url>
                    <DocumentType>CreditCheckReport</DocumentType>
                    <DocumentReference>CreditReport-21 Meridian Road-20160215121822404.html</DocumentReference>
                    <DocumentDate>2016-02-15T12:18:22.45</DocumentDate>
                    <StartDate xsi:nil="true"/>
                    <EndDate xsi:nil="true"/>
                    <Verified>true</Verified>
                </ItpDocument>
                <ItpDocument>
                    <Url>https://project-equalet-documents.s3.amazonaws.com/Test1/1f33ded2-c07d-45a5-be6a-08328194f0f5/Documents/IdCheckReport-0.html</Url>
                    <DocumentType>IdCheckReport</DocumentType>
                    <DocumentReference>IdCheckReport-0.html</DocumentReference>
                    <DocumentDate>2016-02-15T12:17:56.763</DocumentDate>
                    <StartDate xsi:nil="true"/>
                    <EndDate xsi:nil="true"/>
                    <Verified>true</Verified>
                </ItpDocument>
                <ItpDocument>
                    <Url>https://project-equalet-documents.s3.amazonaws.com/Test1/1f33ded2-c07d-45a5-be6a-08328194f0f5/Documents/20160215121832747.pdf</Url>
                    <DocumentType>ProofOfResidence</DocumentType>
                    <DocumentReference>ref-ProofOfResidence</DocumentReference>
                    <DocumentDate xsi:nil="true"/>
                    <StartDate>2015-02-15T12:18:21.987</StartDate>
                    <EndDate>2017-02-15T12:18:21.987</EndDate>
                    <Verified>true</Verified>
                </ItpDocument>
                <ItpDocument>
                    <Url>https://project-equalet-documents.s3.amazonaws.com/Test1/1f33ded2-c07d-45a5-be6a-08328194f0f5/Documents/20160215121832950.pdf</Url>
                    <DocumentType>PhotoId</DocumentType>
                    <DocumentReference>ref-PhotoId</DocumentReference>
                    <DocumentDate xsi:nil="true"/>
                    <StartDate>2015-02-15T12:18:22.207</StartDate>
                    <EndDate>2017-02-15T12:18:22.207</EndDate>
                    <Verified>true</Verified>
                </ItpDocument>
                <ItpDocument>
                    <Url>https://project-equalet-documents.s3.amazonaws.com/Test1/1f33ded2-c07d-45a5-be6a-08328194f0f5/Documents/20160215121833700.pdf</Url>
                    <DocumentType>ImmigrationStatusDoc</DocumentType>
                    <DocumentReference>ref-ImmigrationStatusDoc</DocumentReference>
                    <DocumentDate xsi:nil="true"/>
                    <StartDate>2015-02-15T12:18:22.963</StartDate>
                    <EndDate>2017-02-15T12:18:22.963</EndDate>
                    <Verified>true</Verified>
                </ItpDocument>
            </UserDocuments>
            <ControllingOrganisation>
                <OrganisationStatus>Limited</OrganisationStatus>
                <OrganisationType>Advertising</OrganisationType>
                <RegisteredOrganisationName>TrisHibLet Ltd</RegisteredOrganisationName>
                <TradingName>TrisHibLet</TradingName>
                <LogoUrl>http://images.TestLettings.Property-Portal.uk/b2b/hiblenlets.gif</LogoUrl>
                <RegistrationNumber>11111111</RegistrationNumber>
                <VatNumber>928289676x</VatNumber>
                <CompanyTelephone>0333 006 3000x</CompanyTelephone>
                <CompanyEmail>theteam@TrisHibLet.co.uk</CompanyEmail>
                <Established>2015-10-01T00:00:00</Established>
                <GrossProfit>0.00</GrossProfit>
                <MarketingType>
                    <Value>NoMarketing</Value>
                    <Description>NoMarketing</Description>
                    <Id>2</Id>
                </MarketingType>
                <ShowCoBranding>true</ShowCoBranding>
                <OrganisationUsers list="true">
                    <ItpOrganisationUser>
                        <OrganisationUserType>
                            <Value>OrganisationAdministrator</Value>
                            <Description>Organisation Administrator</Description>
                            <Id>1</Id>
                        </OrganisationUserType>
                        <OrganisationUserRole>
                            <Value>Owner</Value>
                            <Description>Owner</Description>
                            <Id>1</Id>
                        </OrganisationUserRole>
                        <SigningAuthority>true</SigningAuthority>
                        <Contact>
                            <Name>Harold Chrysler</Name>
                            <TelephoneNumber>200680493</TelephoneNumber>
                            <Email>trishiblet@9yds-testing.co.uk</Email>
                            <ContactAddress>
                                <AddressId>5f547622-ded3-e511-81e6-06ab496445e9</AddressId>
                                <AddressLine1>18, Top Gear Lane</AddressLine1>
                                <City>Test Town</City>
                                <Postcode>X9 9LF</Postcode>
                                <CurrentAddress>true</CurrentAddress>
                                <ResidencyStatus>PrivateRented</ResidencyStatus>
                                <ResidencyStatusDesc>Private Rented</ResidencyStatusDesc>
                            </ContactAddress>
                        </Contact>
                    </ItpOrganisationUser>
                    <ItpOrganisationUser>
                        <OrganisationUserType>
                            <Value>OrganisationAdministrator</Value>
                            <Description>Organisation Administrator</Description>
                            <Id>1</Id>
                        </OrganisationUserType>
                        <OrganisationUserRole>
                            <Value>Owner</Value>
                            <Description>Owner</Description>
                            <Id>1</Id>
                        </OrganisationUserRole>
                        <SigningAuthority>true</SigningAuthority>
                        <Contact>
                            <Name>Org Admin</Name>
                            <Email>TrisHibLet@hiblen.com</Email>
                        </Contact>
                    </ItpOrganisationUser>
                </OrganisationUsers>
                <Addresses list="true">
                    <ItpAddress>
                        <AddressId>7f5d7904-68d1-e511-81e5-06ab496445e9</AddressId>
                        <AddressLine1>TrisHibLet</AddressLine1>
                        <AddressLine2>PO box 666</AddressLine2>
                        <City>London</City>
                        <Postcode>SW12 9KL</Postcode>
                        <CurrentAddress>true</CurrentAddress>
                        <ResidencyStatus>Owned</ResidencyStatus>
                        <AddressType>
                            <Value>RegisteredOffice</Value>
                            <Description>RegisteredOffice</Description>
                            <Id>2</Id>
                        </AddressType>
                        <ResidencyStatusDesc>Owned</ResidencyStatusDesc>
                    </ItpAddress>
                    <ItpAddress>
                        <AddressId>805d7904-68d1-e511-81e5-06ab496445e9</AddressId>
                        <AddressLine1>TrisHibLet</AddressLine1>
                        <AddressLine2>PO box 666</AddressLine2>
                        <City>London</City>
                        <Postcode>SW12 9KL</Postcode>
                        <CurrentAddress>true</CurrentAddress>
                        <ResidencyStatus>Owned</ResidencyStatus>
                        <AddressType>
                            <Value>AccountantAddress</Value>
                            <Description>AccountantAddress</Description>
                            <Id>4</Id>
                        </AddressType>
                        <ResidencyStatusDesc>Owned</ResidencyStatusDesc>
                    </ItpAddress>
                </Addresses>
                <BankAccounts list="true">
                    <ItpBank/>
                </BankAccounts>
            </ControllingOrganisation>
            <LandlordType>
                <Value>NotSet</Value>
                <Description>NotSet</Description>
                <Id>0</Id>
            </LandlordType>
            <ReferencingPaid>true</ReferencingPaid>
            <ReferenceCheckStatus>Passed</ReferenceCheckStatus>
            <ReferenceCheckSoftPass>false</ReferenceCheckSoftPass>
            <GuarantorRequired xsi:nil="true"/>
            <GuarantorAdded>false</GuarantorAdded>
            <AgreementSigningStatus>NotSet</AgreementSigningStatus>
            <ConfirmedUser>true</ConfirmedUser>
            <SigningUser>true</SigningUser>
            <AgencyStaff>true</AgencyStaff>
            <NoPasswordEnteredOnRegistration>false</NoPasswordEnteredOnRegistration>
            <TenantWantsDetails>false</TenantWantsDetails>
            <TenantWantsViewing>false</TenantWantsViewing>
            <IsSmoker>false</IsSmoker>
            <HasPets>true</HasPets>
            <HasDependents>true</HasDependents>
            <IsRegisteringDeposit>false</IsRegisteringDeposit>
        </ItpUser>
        <ItpUser>
            <UserId>f1eed456-2530-4ab9-af63-2bc37a7b0d5d</UserId>
            <Title>Dr</Title>
            <FirstName>Sadie</FirstName>
            <LastName>Griffin</LastName>
            <Email>prime_LL20@9yds-testing.co.uk</Email>
            <HomeTel>2101007003</HomeTel>
            <WorkTel>745218734</WorkTel>
            <Mobile>605170075</Mobile>
            <PropertyUserType>
                <Value>PropertyOwner</Value>
                <Description>Property Administrator</Description>
                <Id>1</Id>
            </PropertyUserType>
            <Addresses list="true">
                <ItpAddress>
                    <AddressId>abce465a-d3d3-e511-81e6-06ab496445e9</AddressId>
                    <AddressLine1>20 Meridian Road</AddressLine1>
                    <City>Hayes</City>
                    <Postcode>UB3 4RB</Postcode>
                    <CurrentAddress>true</CurrentAddress>
                    <ResidencyStatus>NotSet</ResidencyStatus>
                    <ResidencyStatusDesc>NotSet</ResidencyStatusDesc>
                </ItpAddress>
            </Addresses>
            <IdCheckStatus>
                <Value>NotChecked</Value>
                <Description>ID Check not yet Performed</Description>
                <Id>0</Id>
            </IdCheckStatus>
            <UserDocuments list="true">
                <ItpDocument>
                    <Url>https://project-equalet-documents.s3.amazonaws.com/Test1/f1eed456-2530-4ab9-af63-2bc37a7b0d5d/Documents/20160215111920054.pdf</Url>
                    <DocumentType>ProofOfResidence</DocumentType>
                    <DocumentReference>ref-ProofOfResidence</DocumentReference>
                    <DocumentDate xsi:nil="true"/>
                    <StartDate>2015-02-12T11:19:09.09</StartDate>
                    <EndDate>2015-02-14T11:19:09.09</EndDate>
                    <Verified>true</Verified>
                </ItpDocument>
                <ItpDocument>
                    <Url>https://project-equalet-documents.s3.amazonaws.com/Test1/f1eed456-2530-4ab9-af63-2bc37a7b0d5d/Documents/20160215111920304.pdf</Url>
                    <DocumentType>PhotoId</DocumentType>
                    <DocumentReference>ref-PhotoId</DocumentReference>
                    <DocumentDate xsi:nil="true"/>
                    <StartDate>2015-02-12T11:19:09.537</StartDate>
                    <EndDate>2015-02-14T11:19:09.537</EndDate>
                    <Verified>true</Verified>
                </ItpDocument>
                <ItpDocument>
                    <Url>https://project-equalet-documents.s3.amazonaws.com/Test1/f1eed456-2530-4ab9-af63-2bc37a7b0d5d/Documents/20160215121805748.pdf</Url>
                    <DocumentType>ProofOfResidence</DocumentType>
                    <DocumentReference>ref-ProofOfResidence</DocumentReference>
                    <DocumentDate xsi:nil="true"/>
                    <StartDate>2015-02-15T12:17:54.903</StartDate>
                    <EndDate>2017-02-15T12:17:54.903</EndDate>
                    <Verified>true</Verified>
                </ItpDocument>
                <ItpDocument>
                    <Url>https://project-equalet-documents.s3.amazonaws.com/Test1/f1eed456-2530-4ab9-af63-2bc37a7b0d5d/Documents/20160215121806513.pdf</Url>
                    <DocumentType>PhotoId</DocumentType>
                    <DocumentReference>ref-PhotoId</DocumentReference>
                    <DocumentDate xsi:nil="true"/>
                    <StartDate>2015-02-15T12:17:55.757</StartDate>
                    <EndDate>2017-02-15T12:17:55.757</EndDate>
                    <Verified>true</Verified>
                </ItpDocument>
            </UserDocuments>
            <ControllingOrganisation>
                <OrganisationStatus>Limited</OrganisationStatus>
                <OrganisationType>Advertising</OrganisationType>
                <RegisteredOrganisationName>Glanty Ltd</RegisteredOrganisationName>
                <TradingName>9yds</TradingName>
                <LogoUrl>https://prime.9yds.co.uk/assets/images/9yds_navbar_logo.png</LogoUrl>
                <RegistrationNumber>05562443</RegistrationNumber>
                <VatNumber>928289676</VatNumber>
                <CompanyTelephone>0333 006 3000</CompanyTelephone>
                <CompanyEmail>theteam@9yds.co.uk</CompanyEmail>
                <Established>2005-01-01T00:00:00</Established>
                <GrossProfit>0.00</GrossProfit>
                <MarketingType>
                    <Value>PropertyPortal</Value>
                    <Description>PropertyPortal</Description>
                    <Id>1</Id>
                </MarketingType>
                <ShowCoBranding>false</ShowCoBranding>
                <OrganisationUsers list="true">
                    <ItpOrganisationUser>
                        <OrganisationUserType>
                            <Value>OrganisationAdministrator</Value>
                            <Description>Organisation Administrator</Description>
                            <Id>1</Id>
                        </OrganisationUserType>
                        <OrganisationUserRole>
                            <Value>Partner</Value>
                            <Description>Partner</Description>
                            <Id>2</Id>
                        </OrganisationUserRole>
                        <SigningAuthority>true</SigningAuthority>
                        <Contact>
                            <Name>Prime Test</Name>
                            <Email>primeadmin@9yds-testing.co.uk</Email>
                        </Contact>
                    </ItpOrganisationUser>
                </OrganisationUsers>
                <Addresses list="true">
                    <ItpAddress>
                        <AddressId>785d7904-68d1-e511-81e5-06ab496445e9</AddressId>
                        <AddressLine1>9yds</AddressLine1>
                        <AddressLine2>PO box 459</AddressLine2>
                        <City>Gravesend</City>
                        <Postcode>DA12 9JW</Postcode>
                        <CurrentAddress>true</CurrentAddress>
                        <ResidencyStatus>Owned</ResidencyStatus>
                        <AddressType>
                            <Value>RegisteredOffice</Value>
                            <Description>RegisteredOffice</Description>
                            <Id>2</Id>
                        </AddressType>
                        <ResidencyStatusDesc>Owned</ResidencyStatusDesc>
                    </ItpAddress>
                    <ItpAddress>
                        <AddressId>795d7904-68d1-e511-81e5-06ab496445e9</AddressId>
                        <AddressLine1>9yds</AddressLine1>
                        <AddressLine2>PO box 459</AddressLine2>
                        <City>Gravesend</City>
                        <Postcode>DA12 9JW</Postcode>
                        <CurrentAddress>true</CurrentAddress>
                        <ResidencyStatus>Owned</ResidencyStatus>
                        <AddressType>
                            <Value>AccountantAddress</Value>
                            <Description>AccountantAddress</Description>
                            <Id>4</Id>
                        </AddressType>
                        <ResidencyStatusDesc>Owned</ResidencyStatusDesc>
                    </ItpAddress>
                </Addresses>
                <BankAccounts list="true">
                    <ItpBank/>
                </BankAccounts>
            </ControllingOrganisation>
            <LandlordType>
                <Value>UnManagedPropertyAdministrator</Value>
                <Description>Where a property administrator registers with the site directly</Description>
                <Id>3</Id>
            </LandlordType>
            <ReferencingPaid xsi:nil="true"/>
            <ReferenceCheckStatus>NotChecked</ReferenceCheckStatus>
            <ReferenceCheckSoftPass xsi:nil="true"/>
            <GuarantorRequired xsi:nil="true"/>
            <GuarantorAdded xsi:nil="true"/>
            <AgreementSigningStatus>NotSet</AgreementSigningStatus>
            <ConfirmedUser>true</ConfirmedUser>
            <SigningUser>true</SigningUser>
            <AgencyStaff>false</AgencyStaff>
            <NoPasswordEnteredOnRegistration>false</NoPasswordEnteredOnRegistration>
            <TenantWantsDetails>false</TenantWantsDetails>
            <TenantWantsViewing>false</TenantWantsViewing>
            <IsSmoker>false</IsSmoker>
            <HasPets>false</HasPets>
            <HasDependents>false</HasDependents>
            <IsRegisteringDeposit>true</IsRegisteringDeposit>
        </ItpUser>
    </PropertyUsers>
</ItpDocumentRequest>
'''
