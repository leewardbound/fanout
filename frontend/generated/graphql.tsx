import { gql } from '@apollo/client';
import * as Apollo from '@apollo/client';
export type Maybe<T> = T | null;
export type Exact<T extends { [key: string]: unknown }> = { [K in keyof T]: T[K] };
/** All built-in and custom scalars, mapped to their actual values */
export type Scalars = {
  ID: string;
  String: string;
  Boolean: boolean;
  Int: number;
  Float: number;
  DateTime: any;
  ExpectedErrorType: any;
  GenericScalar: any;
  JSONString: any;
  UUID: any;
};

export type Activity = {
  __typename?: 'Activity';
  createdAt: Scalars['DateTime'];
  id: Scalars['String'];
  image?: Maybe<Image>;
  note?: Maybe<Note>;
  objectId?: Maybe<Scalars['String']>;
  objectType?: Maybe<Scalars['String']>;
  payload?: Maybe<Scalars['JSONString']>;
  relatedObjectId?: Maybe<Scalars['String']>;
  targetId?: Maybe<Scalars['String']>;
  updatedAt: Scalars['DateTime'];
  verb: ActivityVerb;
};

export enum ActivityVerb {
  Accept = 'ACCEPT',
  Add = 'ADD',
  Announce = 'ANNOUNCE',
  Arrive = 'ARRIVE',
  Block = 'BLOCK',
  Create = 'CREATE',
  Delete = 'DELETE',
  Dislike = 'DISLIKE',
  Flag = 'FLAG',
  Follow = 'FOLLOW',
  Ignore = 'IGNORE',
  Invite = 'INVITE',
  Join = 'JOIN',
  Leave = 'LEAVE',
  Like = 'LIKE',
  Listen = 'LISTEN',
  Move = 'MOVE',
  Offer = 'OFFER',
  Question = 'QUESTION',
  Read = 'READ',
  Reject = 'REJECT',
  Remove = 'REMOVE',
  Share = 'SHARE',
  Tentativeaccept = 'TENTATIVEACCEPT',
  Tentativereject = 'TENTATIVEREJECT',
  Travel = 'TRAVEL',
  Undo = 'UNDO',
  Update = 'UPDATE',
  View = 'VIEW'
}

export type CreateNote = {
  __typename?: 'CreateNote';
  activity?: Maybe<Activity>;
};

export type CreateNoteInput = {
  actorId: Scalars['String'];
  content: Scalars['String'];
};

export type CreateUserInput = {
  email: Scalars['String'];
  firstName: Scalars['String'];
  lastName: Scalars['String'];
};

export type CreateUserResult = Error | UserProfile;

export type Customer = {
  __typename?: 'Customer';
  createdAt: Scalars['DateTime'];
  datapoints?: Maybe<Array<Maybe<CustomerDataPoint>>>;
  email?: Maybe<Scalars['String']>;
  id: Scalars['UUID'];
  relatedUser?: Maybe<UserProfile>;
  updatedAt: Scalars['DateTime'];
};

export type CustomerDataPoint = {
  __typename?: 'CustomerDataPoint';
  key?: Maybe<Scalars['String']>;
  value?: Maybe<Scalars['String']>;
};

export type CustomerDataPointInput = {
  key: Scalars['String'];
  value: Scalars['String'];
};


export type Error = {
  __typename?: 'Error';
  message: Scalars['String'];
};



export type Image = {
  __typename?: 'Image';
  contentUrl: Scalars['String'];
  createdAt: Scalars['DateTime'];
  id: Scalars['String'];
  updatedAt: Scalars['DateTime'];
};


export type Mutation = {
  __typename?: 'Mutation';
  createNote?: Maybe<CreateNote>;
  createUser?: Maybe<CreateUserResult>;
  passwordChange?: Maybe<PasswordChange>;
  passwordReset?: Maybe<PasswordReset>;
  refreshToken?: Maybe<RefreshToken>;
  register?: Maybe<Register>;
  resendActivationEmail?: Maybe<ResendActivationEmail>;
  sendPasswordResetEmail?: Maybe<SendPasswordResetEmail>;
  subscribeByEmail?: Maybe<SubscribeByEmail>;
  tokenAuth?: Maybe<ObtainJsonWebToken>;
  updateAccount?: Maybe<UpdateAccount>;
  verifyAccount?: Maybe<VerifyAccount>;
  verifyToken?: Maybe<VerifyToken>;
};


export type MutationCreateNoteArgs = {
  input?: Maybe<CreateNoteInput>;
};


export type MutationCreateUserArgs = {
  input?: Maybe<CreateUserInput>;
};


export type MutationPasswordChangeArgs = {
  newPassword1: Scalars['String'];
  newPassword2: Scalars['String'];
  oldPassword: Scalars['String'];
};


export type MutationPasswordResetArgs = {
  newPassword1: Scalars['String'];
  newPassword2: Scalars['String'];
  token: Scalars['String'];
};


export type MutationRefreshTokenArgs = {
  refreshToken: Scalars['String'];
};


export type MutationRegisterArgs = {
  email: Scalars['String'];
  firstName: Scalars['String'];
  lastName: Scalars['String'];
  password1: Scalars['String'];
  password2: Scalars['String'];
  username: Scalars['String'];
};


export type MutationResendActivationEmailArgs = {
  email: Scalars['String'];
};


export type MutationSendPasswordResetEmailArgs = {
  email: Scalars['String'];
};


export type MutationSubscribeByEmailArgs = {
  input?: Maybe<SubscribeByEmailInput>;
};


export type MutationTokenAuthArgs = {
  email_Iexact?: Maybe<Scalars['String']>;
  password: Scalars['String'];
  username_Iexact?: Maybe<Scalars['String']>;
};


export type MutationUpdateAccountArgs = {
  firstName?: Maybe<Scalars['String']>;
  lastName?: Maybe<Scalars['String']>;
};


export type MutationVerifyAccountArgs = {
  token: Scalars['String'];
};


export type MutationVerifyTokenArgs = {
  token: Scalars['String'];
};

export type Node = {
  id: Scalars['ID'];
};

export type Note = {
  __typename?: 'Note';
  content: Scalars['String'];
  createdAt: Scalars['DateTime'];
  id: Scalars['String'];
  updatedAt: Scalars['DateTime'];
};

export type ObtainJsonWebToken = {
  __typename?: 'ObtainJSONWebToken';
  errors?: Maybe<Scalars['ExpectedErrorType']>;
  refreshToken?: Maybe<Scalars['String']>;
  success?: Maybe<Scalars['Boolean']>;
  token?: Maybe<Scalars['String']>;
  unarchiving?: Maybe<Scalars['Boolean']>;
  user?: Maybe<UserNode>;
};

export type PasswordChange = {
  __typename?: 'PasswordChange';
  errors?: Maybe<Scalars['ExpectedErrorType']>;
  refreshToken?: Maybe<Scalars['String']>;
  success?: Maybe<Scalars['Boolean']>;
  token?: Maybe<Scalars['String']>;
};

export type PasswordReset = {
  __typename?: 'PasswordReset';
  errors?: Maybe<Scalars['ExpectedErrorType']>;
  success?: Maybe<Scalars['Boolean']>;
};

export type Query = {
  __typename?: 'Query';
  activities?: Maybe<Array<Maybe<Activity>>>;
  myProfile?: Maybe<UserProfile>;
};


export type QueryActivitiesArgs = {
  actorId: Scalars['ID'];
};

export type RefreshToken = {
  __typename?: 'RefreshToken';
  errors?: Maybe<Scalars['ExpectedErrorType']>;
  payload?: Maybe<Scalars['GenericScalar']>;
  refreshToken?: Maybe<Scalars['String']>;
  success?: Maybe<Scalars['Boolean']>;
  token?: Maybe<Scalars['String']>;
};

export type Register = {
  __typename?: 'Register';
  errors?: Maybe<Scalars['ExpectedErrorType']>;
  refreshToken?: Maybe<Scalars['String']>;
  success?: Maybe<Scalars['Boolean']>;
  token?: Maybe<Scalars['String']>;
};

export type ResendActivationEmail = {
  __typename?: 'ResendActivationEmail';
  errors?: Maybe<Scalars['ExpectedErrorType']>;
  success?: Maybe<Scalars['Boolean']>;
};

export type SendPasswordResetEmail = {
  __typename?: 'SendPasswordResetEmail';
  errors?: Maybe<Scalars['ExpectedErrorType']>;
  success?: Maybe<Scalars['Boolean']>;
};

export type SubscribeByEmail = {
  __typename?: 'SubscribeByEmail';
  created?: Maybe<Scalars['Boolean']>;
  datapoints?: Maybe<Array<Maybe<CustomerDataPoint>>>;
  email?: Maybe<Scalars['String']>;
};

export type SubscribeByEmailInput = {
  actorId: Scalars['String'];
  datapoints?: Maybe<Array<Maybe<CustomerDataPointInput>>>;
  email: Scalars['String'];
};


export type UpdateAccount = {
  __typename?: 'UpdateAccount';
  errors?: Maybe<Scalars['ExpectedErrorType']>;
  success?: Maybe<Scalars['Boolean']>;
};

export type UserNode = Node & {
  __typename?: 'UserNode';
  archived?: Maybe<Scalars['Boolean']>;
  createdAt: Scalars['DateTime'];
  dateJoined: Scalars['DateTime'];
  email: Scalars['String'];
  firstName: Scalars['String'];
  id: Scalars['ID'];
  isActive: Scalars['Boolean'];
  isStaff: Scalars['Boolean'];
  lastLogin?: Maybe<Scalars['DateTime']>;
  lastName: Scalars['String'];
  pk?: Maybe<Scalars['Int']>;
  relatedCustomer?: Maybe<Customer>;
  secondaryEmail?: Maybe<Scalars['String']>;
  updatedAt: Scalars['DateTime'];
  username: Scalars['String'];
  verified?: Maybe<Scalars['Boolean']>;
};

export type UserProfile = {
  __typename?: 'UserProfile';
  email: Scalars['String'];
  firstName: Scalars['String'];
  id: Scalars['UUID'];
  isStaff: Scalars['Boolean'];
  lastName: Scalars['String'];
  username: Scalars['String'];
  verified?: Maybe<Scalars['Boolean']>;
};

export type VerifyAccount = {
  __typename?: 'VerifyAccount';
  errors?: Maybe<Scalars['ExpectedErrorType']>;
  success?: Maybe<Scalars['Boolean']>;
};

export type VerifyToken = {
  __typename?: 'VerifyToken';
  errors?: Maybe<Scalars['ExpectedErrorType']>;
  payload?: Maybe<Scalars['GenericScalar']>;
  success?: Maybe<Scalars['Boolean']>;
};

export type UserProfileFragment = { __typename?: 'UserProfile', id: any, firstName: string, lastName: string, email: string, username: string };

export type MyProfileQueryVariables = Exact<{ [key: string]: never; }>;


export type MyProfileQuery = { __typename?: 'Query', myProfile?: Maybe<(
    { __typename?: 'UserProfile' }
    & UserProfileFragment
  )> };

export const UserProfileFragmentDoc = gql`
    fragment UserProfile on UserProfile {
  id
  firstName
  lastName
  email
  username
}
    `;
export const MyProfileDocument = gql`
    query myProfile {
  myProfile {
    ...UserProfile
  }
}
    ${UserProfileFragmentDoc}`;

/**
 * __useMyProfileQuery__
 *
 * To run a query within a React component, call `useMyProfileQuery` and pass it any options that fit your needs.
 * When your component renders, `useMyProfileQuery` returns an object from Apollo Client that contains loading, error, and data properties
 * you can use to render your UI.
 *
 * @param baseOptions options that will be passed into the query, supported options are listed on: https://www.apollographql.com/docs/react/api/react-hooks/#options;
 *
 * @example
 * const { data, loading, error } = useMyProfileQuery({
 *   variables: {
 *   },
 * });
 */
export function useMyProfileQuery(baseOptions?: Apollo.QueryHookOptions<MyProfileQuery, MyProfileQueryVariables>) {
        return Apollo.useQuery<MyProfileQuery, MyProfileQueryVariables>(MyProfileDocument, baseOptions);
      }
export function useMyProfileLazyQuery(baseOptions?: Apollo.LazyQueryHookOptions<MyProfileQuery, MyProfileQueryVariables>) {
          return Apollo.useLazyQuery<MyProfileQuery, MyProfileQueryVariables>(MyProfileDocument, baseOptions);
        }
export type MyProfileQueryHookResult = ReturnType<typeof useMyProfileQuery>;
export type MyProfileLazyQueryHookResult = ReturnType<typeof useMyProfileLazyQuery>;
export type MyProfileQueryResult = Apollo.QueryResult<MyProfileQuery, MyProfileQueryVariables>;